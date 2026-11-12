// Package share exposes the local showcase through a temporary public tunnel.
//
// The manager owns exactly one cloudflared quick-tunnel process. A tunnel is
// deliberately ephemeral: it is started on demand, has no account or custom
// hostname, and is killed when sharing is stopped or the API shuts down.
package share

import (
	"bufio"
	"context"
	"errors"
	"fmt"
	"io"
	"os/exec"
	"regexp"
	"strings"
	"sync"
	"time"
)

const Provider = "cloudflare-quick-tunnel"

var (
	// ErrUnavailable means the cloudflared binary could not be found.
	ErrUnavailable = errors.New("cloudflared is not installed")
	// ErrTimeout means cloudflared did not publish a public URL in time.
	ErrTimeout = errors.New("timed out waiting for a share link")
	// ErrStarting means another start request is already in flight.
	ErrStarting = errors.New("a share link is already being generated")
)

// A quick tunnel always lands on an unguessable *.trycloudflare.com hostname.
var tunnelURL = regexp.MustCompile(`https://[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.trycloudflare\.com`)

// Status is the public, side-effect-free view of the share manager. It never
// contains process ids, file paths or credentials.
type Status struct {
	Active    bool       `json:"active"`
	Starting  bool       `json:"starting"`
	URL       string     `json:"url,omitempty"`
	Provider  string     `json:"provider"`
	Target    string     `json:"target"`
	Available bool       `json:"available"`
	StartedAt *time.Time `json:"startedAt,omitempty"`
	Message   string     `json:"message,omitempty"`
}

// Manager starts and stops the one allowed quick tunnel.
type Manager struct {
	bin    string
	target string

	mu        sync.Mutex
	cmd       *exec.Cmd
	done      chan struct{}
	url       string
	startedAt time.Time
	starting  bool
	message   string
	tail      []string
}

// New returns a manager for the given cloudflared binary and local target URL.
func New(bin, target string) *Manager {
	if strings.TrimSpace(bin) == "" {
		bin = "cloudflared"
	}
	return &Manager{bin: bin, target: target}
}

// Status reports the current tunnel without touching the network.
func (m *Manager) Status() Status {
	m.mu.Lock()
	defer m.mu.Unlock()
	return m.statusLocked()
}

func (m *Manager) statusLocked() Status {
	status := Status{
		Active:    m.cmd != nil && m.url != "",
		Starting:  m.starting,
		URL:       m.url,
		Provider:  Provider,
		Target:    m.target,
		Available: true,
		Message:   m.message,
	}
	if _, err := exec.LookPath(m.bin); err != nil {
		status.Available = false
		if status.Message == "" {
			status.Message = "cloudflared was not found on PATH"
		}
	}
	if m.cmd != nil && !m.startedAt.IsZero() {
		started := m.startedAt
		status.StartedAt = &started
	}
	return status
}

// Start launches cloudflared and waits for its public hostname. It is
// idempotent while a tunnel is live.
func (m *Manager) Start(ctx context.Context) (Status, error) {
	m.mu.Lock()
	if m.cmd != nil && m.url != "" {
		status := m.statusLocked()
		m.mu.Unlock()
		return status, nil
	}
	if m.starting {
		status := m.statusLocked()
		m.mu.Unlock()
		return status, ErrStarting
	}
	if _, err := exec.LookPath(m.bin); err != nil {
		status := m.statusLocked()
		m.mu.Unlock()
		return status, ErrUnavailable
	}

	cmd := exec.Command(m.bin, "tunnel", "--url", m.target, "--no-autoupdate")
	stdout, err := cmd.StdoutPipe()
	if err != nil {
		m.mu.Unlock()
		return m.statusLocked(), fmt.Errorf("prepare cloudflared stdout: %w", err)
	}
	stderr, err := cmd.StderrPipe()
	if err != nil {
		m.mu.Unlock()
		return m.statusLocked(), fmt.Errorf("prepare cloudflared stderr: %w", err)
	}
	if err := cmd.Start(); err != nil {
		m.mu.Unlock()
		return m.statusLocked(), fmt.Errorf("start cloudflared: %w", err)
	}

	done := make(chan struct{})
	m.cmd = cmd
	m.done = done
	m.url = ""
	m.startedAt = time.Now()
	m.starting = true
	m.message = ""
	m.tail = nil
	m.mu.Unlock()

	urls := make(chan string, 1)
	var readers sync.WaitGroup
	readers.Add(2)
	scan := func(reader io.Reader) {
		defer readers.Done()
		scanner := bufio.NewScanner(reader)
		scanner.Buffer(make([]byte, 64*1024), 1<<20)
		for scanner.Scan() {
			line := scanner.Text()
			m.recordTail(line)
			if url := extractURL(line); url != "" {
				select {
				case urls <- url:
				default:
				}
			}
		}
	}
	go scan(stdout)
	go scan(stderr)

	go func() {
		readers.Wait()
		waitErr := cmd.Wait()
		close(done)

		m.mu.Lock()
		if m.cmd == cmd {
			if m.url == "" {
				m.message = "cloudflared stopped before publishing a link"
				if reason := m.lastErrorLocked(); reason != "" {
					m.message += ": " + reason
				} else if waitErr != nil {
					m.message += ": " + waitErr.Error()
				}
			} else {
				m.message = "The share link was stopped"
			}
			m.cmd = nil
			m.done = nil
			m.url = ""
			m.starting = false
		}
		m.mu.Unlock()
	}()

	timer := time.NewTimer(45 * time.Second)
	defer timer.Stop()

	select {
	case url := <-urls:
		m.mu.Lock()
		if m.cmd == cmd {
			m.url = url
			m.starting = false
			m.message = ""
		}
		m.mu.Unlock()

		// Cloudflare occasionally publishes a hostname and then closes the
		// tunnel immediately (rate limits, edge handshake failures). A short
		// stability window avoids handing out a link that is already dead.
		stable := time.NewTimer(900 * time.Millisecond)
		defer stable.Stop()
		select {
		case <-done:
			m.mu.Lock()
			status := m.statusLocked()
			message := m.message
			m.mu.Unlock()
			if message == "" {
				message = "cloudflared exited immediately after publishing a link"
			}
			return status, errors.New(message)
		case <-ctx.Done():
			_ = cmd.Process.Kill()
			return m.Status(), ctx.Err()
		case <-stable.C:
			m.mu.Lock()
			status := m.statusLocked()
			active := m.cmd == cmd && m.url != ""
			m.mu.Unlock()
			if !active {
				return status, errors.New("cloudflared stopped before the link was ready")
			}
			return status, nil
		}
	case <-done:
		m.mu.Lock()
		status := m.statusLocked()
		message := m.message
		m.mu.Unlock()
		if message == "" {
			message = "cloudflared stopped before the link was ready"
		}
		return status, errors.New(message)
	case <-timer.C:
		_ = cmd.Process.Kill()
		m.mu.Lock()
		m.message = "Timed out waiting for cloudflared to publish a link"
		m.mu.Unlock()
		return m.Status(), ErrTimeout
	case <-ctx.Done():
		_ = cmd.Process.Kill()
		return m.Status(), ctx.Err()
	}
}

// Stop ends the active tunnel. It is safe to call when nothing is running.
func (m *Manager) Stop() error {
	m.mu.Lock()
	cmd := m.cmd
	done := m.done
	m.mu.Unlock()
	if cmd == nil {
		return nil
	}
	if cmd.Process != nil {
		_ = cmd.Process.Kill()
	}
	if done != nil {
		select {
		case <-done:
		case <-time.After(5 * time.Second):
		}
	}
	m.mu.Lock()
	if m.cmd == cmd {
		m.cmd = nil
		m.done = nil
		m.url = ""
		m.starting = false
	}
	m.message = "The share link was stopped"
	m.mu.Unlock()
	return nil
}

// Close is an alias for Stop, used on API shutdown.
func (m *Manager) Close() error { return m.Stop() }

func (m *Manager) recordTail(line string) {
	line = strings.TrimSpace(line)
	if line == "" {
		return
	}
	m.mu.Lock()
	m.tail = append(m.tail, line)
	if len(m.tail) > 12 {
		m.tail = m.tail[len(m.tail)-12:]
	}
	m.mu.Unlock()
}

func (m *Manager) lastErrorLocked() string {
	for i := len(m.tail) - 1; i >= 0; i-- {
		line := m.tail[i]
		if strings.Contains(line, "ERR") || strings.Contains(strings.ToLower(line), "error") {
			if len(line) > 220 {
				line = line[:220] + "…"
			}
			return line
		}
	}
	return ""
}

func extractURL(line string) string {
	return tunnelURL.FindString(line)
}
