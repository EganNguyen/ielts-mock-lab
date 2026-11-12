package share

import (
	"context"
	"errors"
	"os"
	"path/filepath"
	"runtime"
	"testing"
	"time"
)

func TestExtractURL(t *testing.T) {
	cases := []struct {
		line string
		want string
	}{
		{"2026-11-12T07:40:08Z INF |  https://culture-cage-providing-state.trycloudflare.com  |", "https://culture-cage-providing-state.trycloudflare.com"},
		{"INF +--------------------------------------------------------------------------------------------+", ""},
		{"https://not-a-tunnel.example.com", ""},
		{"https://UPPER.trycloudflare.com", ""},
	}
	for _, tc := range cases {
		if got := extractURL(tc.line); got != tc.want {
			t.Fatalf("extractURL(%q) = %q, want %q", tc.line, got, tc.want)
		}
	}
}

func TestStartAndStopWithFakeTunnel(t *testing.T) {
	if runtime.GOOS == "windows" {
		t.Skip("shell script fixture is POSIX-only")
	}
	dir := t.TempDir()
	bin := filepath.Join(dir, "fake-cloudflared")
	script := "#!/bin/sh\nprintf 'INF |  https://unit-test-share.trycloudflare.com  |\\n'\nexec sleep 30\n"
	if err := os.WriteFile(bin, []byte(script), 0o755); err != nil {
		t.Fatal(err)
	}

	manager := New(bin, "http://127.0.0.1:3000")
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	status, err := manager.Start(ctx)
	if err != nil {
		t.Fatalf("Start: %v", err)
	}
	if !status.Active || status.URL != "https://unit-test-share.trycloudflare.com" {
		t.Fatalf("unexpected status after start: %+v", status)
	}
	if !status.Available {
		t.Fatalf("expected fake binary to be available: %+v", status)
	}

	again, err := manager.Start(ctx)
	if err != nil {
		t.Fatalf("second Start should be idempotent: %v", err)
	}
	if again.URL != status.URL {
		t.Fatalf("second Start returned %q, want %q", again.URL, status.URL)
	}

	if err := manager.Stop(); err != nil {
		t.Fatalf("Stop: %v", err)
	}
	if stopped := manager.Status(); stopped.Active || stopped.URL != "" {
		t.Fatalf("tunnel still active after Stop: %+v", stopped)
	}
}

func TestUnavailableBinary(t *testing.T) {
	manager := New(filepath.Join(t.TempDir(), "missing-cloudflared"), "http://127.0.0.1:3000")
	if status := manager.Status(); status.Available {
		t.Fatalf("expected unavailable status, got %+v", status)
	}
	if _, err := manager.Start(context.Background()); !errors.Is(err, ErrUnavailable) {
		t.Fatalf("Start error = %v, want ErrUnavailable", err)
	}
}
