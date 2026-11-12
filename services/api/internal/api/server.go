package api

import (
	"context"
	"crypto/rand"
	"crypto/sha256"
	"encoding/base64"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"log/slog"
	"net"
	"net/http"
	"net/url"
	"os"
	"path/filepath"
	"strings"
	"time"

	"apex/api/internal/content"
	"apex/api/internal/db"
	"apex/api/internal/model"
	"apex/api/internal/share"
)

type Server struct {
	store     *db.Store
	exams     []model.Exam
	demoMode  bool
	mediaDir  string
	logger    *slog.Logger
	webOrigin string
	share     *share.Manager
}

func New(store *db.Store, exams []model.Exam, demoMode bool, mediaDir string, logger *slog.Logger) *Server {
	webOrigin := env("WEB_ORIGIN", "http://127.0.0.1:3000")
	return &Server{
		store: store, exams: exams, demoMode: demoMode, mediaDir: mediaDir, logger: logger,
		webOrigin: webOrigin,
		share:     share.New(env("CLOUDFLARED_BIN", "cloudflared"), env("SHARE_TARGET", webOrigin)),
	}
}

// Close releases the public share tunnel, if one is running.
func (s *Server) Close() error { return s.share.Close() }

func (s *Server) Handler() http.Handler {
	mux := http.NewServeMux()
	mux.HandleFunc("GET /api/v1/health", s.health)
	mux.HandleFunc("GET /api/v1/config", s.config)
	mux.HandleFunc("GET /api/v1/share", s.getShare)
	mux.HandleFunc("POST /api/v1/share", s.startShare)
	mux.HandleFunc("DELETE /api/v1/share", s.stopShare)
	mux.HandleFunc("POST /api/v1/auth/register", s.register)
	mux.HandleFunc("POST /api/v1/auth/login", s.login)
	mux.HandleFunc("POST /api/v1/auth/logout", s.logout)
	mux.HandleFunc("GET /api/v1/auth/me", s.me)
	mux.HandleFunc("GET /api/v1/exams", s.listExams)
	mux.HandleFunc("GET /api/v1/exams/{id}", s.getExam)
	mux.HandleFunc("POST /api/v1/exams/{id}/attempts", s.createAttempt)
	mux.HandleFunc("GET /api/v1/attempts/active", s.activeAttempt)
	mux.HandleFunc("GET /api/v1/attempts/{id}", s.getAttempt)
	mux.HandleFunc("POST /api/v1/attempts/{id}/sections/{skill}/start", s.startSection)
	mux.HandleFunc("PUT /api/v1/attempts/{id}/sections/{skill}/answers/{questionId}", s.saveAnswer)
	mux.HandleFunc("POST /api/v1/attempts/{id}/sections/{skill}/submit", s.submitSection)
	mux.HandleFunc("POST /api/v1/attempts/{id}/speaking", s.speakingResponse)
	mux.HandleFunc("POST /api/v1/attempts/{id}/complete", s.completeAttempt)
	mux.HandleFunc("GET /api/v1/attempts/{id}/results", s.getResult)
	mux.HandleFunc("GET /api/v1/attempts/{id}/review", s.getReview)
	mux.HandleFunc("GET /api/v1/history", s.history)
	mux.HandleFunc("GET /api/v1/admin/summary", s.adminSummary)

	media := http.FileServer(http.Dir(s.mediaDir))
	mux.Handle("GET /media/", http.StripPrefix("/media/", media))

	return s.recoverer(s.cors(s.logging(mux)))
}

func (s *Server) health(w http.ResponseWriter, r *http.Request) {
	ctx, cancel := context.WithTimeout(r.Context(), 2*time.Second)
	defer cancel()
	dbOK := true
	if err := s.store.Pool.Ping(ctx); err != nil {
		dbOK = false
	}
	writeJSON(w, http.StatusOK, map[string]any{
		"status": "ok", "database": dbOK, "service": "apex-api", "time": time.Now().UTC(),
		"demoMode": s.demoMode, "evaluationProvider": "local-rubric-v1", "speechProvider": "kokoro-82m-onnx", "transcriptionProvider": "browser-speech-recognition-optional",
	})
}

func (s *Server) config(w http.ResponseWriter, r *http.Request) {
	writeJSON(w, http.StatusOK, map[string]any{
		"demoMode": s.demoMode, "evaluationProvider": "local-rubric-v1",
		"speechProvider": "kokoro-82m-onnx", "transcriptionProvider": "browser-speech-recognition-optional", "officialScores": false,
	})
}

// getShare is intentionally unauthenticated: it only reveals the public
// hostname that the local operator chose to create. It never reveals a process
// id, command line or local filesystem path.
func (s *Server) getShare(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Cache-Control", "no-store")
	writeJSON(w, http.StatusOK, s.share.Status())
}

func (s *Server) startShare(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Cache-Control", "no-store")
	if !s.demoMode {
		writeError(w, http.StatusConflict, "SHARE_REQUIRES_DEMO", "Public share links are only available in local demo mode")
		return
	}
	if !s.allowShareControl(r) {
		writeError(w, http.StatusForbidden, "LOCAL_CONTROL_REQUIRED", "Generate the share link from the local app on this machine")
		return
	}
	ctx, cancel := context.WithTimeout(r.Context(), 50*time.Second)
	defer cancel()
	status, err := s.share.Start(ctx)
	if err != nil {
		code := "SHARE_FAILED"
		httpStatus := http.StatusBadGateway
		switch {
		case errors.Is(err, share.ErrUnavailable):
			code, httpStatus = "SHARE_UNAVAILABLE", http.StatusServiceUnavailable
		case errors.Is(err, share.ErrTimeout):
			code, httpStatus = "SHARE_TIMEOUT", http.StatusGatewayTimeout
		case errors.Is(err, share.ErrStarting):
			code, httpStatus = "SHARE_STARTING", http.StatusConflict
		}
		s.logger.Warn("start share link", "err", err)
		writeError(w, httpStatus, code, err.Error())
		return
	}
	s.logger.Info("share link started", "url", status.URL)
	writeJSON(w, http.StatusOK, status)
}

func (s *Server) stopShare(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Cache-Control", "no-store")
	if !s.allowShareControl(r) {
		writeError(w, http.StatusForbidden, "LOCAL_CONTROL_REQUIRED", "Stop the share link from the local app on this machine")
		return
	}
	if err := s.share.Stop(); err != nil {
		s.fail(w, err)
		return
	}
	s.logger.Info("share link stopped")
	writeJSON(w, http.StatusOK, s.share.Status())
}

// allowShareControl limits tunnel management to a page served from loopback.
// A request that arrived through Cloudflare carries a CF-* header, so a visitor
// who receives the public link cannot start or stop the tunnel.
func (s *Server) allowShareControl(r *http.Request) bool {
	if r.Header.Get("CF-Connecting-IP") != "" || r.Header.Get("CF-Ray") != "" || r.Header.Get("CF-Visitor") != "" {
		return false
	}
	remote, _, err := net.SplitHostPort(r.RemoteAddr)
	if err != nil || (remote != "127.0.0.1" && remote != "::1") {
		return false
	}
	return isLoopbackOrigin(r.Header.Get("Origin"))
}

func isLoopbackOrigin(origin string) bool {
	if origin == "" {
		return false
	}
	parsed, err := url.Parse(origin)
	if err != nil || parsed.Scheme == "" || parsed.Host == "" {
		return false
	}
	switch strings.ToLower(parsed.Hostname()) {
	case "127.0.0.1", "localhost", "::1":
		return true
	default:
		return false
	}
}

func (s *Server) listExams(w http.ResponseWriter, r *http.Request) {
	exams, err := s.store.ListExams(r.Context())
	if err != nil {
		s.fail(w, err)
		return
	}
	writeJSON(w, http.StatusOK, map[string]any{"exams": exams})
}

func (s *Server) getExam(w http.ResponseWriter, r *http.Request) {
	exam, err := s.store.GetExamPublic(r.Context(), r.PathValue("id"))
	if err != nil {
		s.fail(w, err)
		return
	}
	writeJSON(w, http.StatusOK, exam)
}

func (s *Server) createAttempt(w http.ResponseWriter, r *http.Request) {
	user, ok := s.requireUser(w, r)
	if !ok {
		return
	}
	var body struct {
		Mode string `json:"mode"`
	}
	_ = decode(r, &body)
	id, err := s.store.CreateAttempt(r.Context(), user.ID, r.PathValue("id"), body.Mode)
	if err != nil {
		s.fail(w, err)
		return
	}
	skill := body.Mode
	if skill == "" || skill == "full" {
		skill = "listening"
	}
	if err := s.store.StartSection(r.Context(), user.ID, id, skill); err != nil {
		s.fail(w, err)
		return
	}
	state, err := s.store.GetState(r.Context(), user.ID, id)
	if err != nil {
		s.fail(w, err)
		return
	}
	s.audit(r.Context(), user.ID, "attempt.create", "attempt", id)
	writeJSON(w, http.StatusCreated, state)
}

func (s *Server) activeAttempt(w http.ResponseWriter, r *http.Request) {
	user, ok := s.requireUser(w, r)
	if !ok {
		return
	}
	attempt, err := s.store.ActiveAttempt(r.Context(), user.ID)
	if err != nil {
		s.fail(w, err)
		return
	}
	writeJSON(w, http.StatusOK, map[string]any{"attempt": attempt})
}

func (s *Server) getAttempt(w http.ResponseWriter, r *http.Request) {
	user, ok := s.requireUser(w, r)
	if !ok {
		return
	}
	state, err := s.store.GetState(r.Context(), user.ID, r.PathValue("id"))
	if err != nil {
		s.fail(w, err)
		return
	}
	writeJSON(w, http.StatusOK, state)
}

func (s *Server) startSection(w http.ResponseWriter, r *http.Request) {
	user, ok := s.requireUser(w, r)
	if !ok {
		return
	}
	if err := s.store.StartSection(r.Context(), user.ID, r.PathValue("id"), r.PathValue("skill")); err != nil {
		s.fail(w, err)
		return
	}
	state, err := s.store.GetState(r.Context(), user.ID, r.PathValue("id"))
	if err != nil {
		s.fail(w, err)
		return
	}
	writeJSON(w, http.StatusOK, state)
}

func (s *Server) saveAnswer(w http.ResponseWriter, r *http.Request) {
	user, ok := s.requireUser(w, r)
	if !ok {
		return
	}
	var body struct {
		Value   string `json:"value"`
		Version int    `json:"version"`
	}
	if err := decode(r, &body); err != nil {
		writeError(w, http.StatusBadRequest, "INVALID_BODY", err.Error())
		return
	}
	answer, err := s.store.SaveAnswer(r.Context(), user.ID, r.PathValue("id"), r.PathValue("skill"), r.PathValue("questionId"), body.Value, body.Version)
	if err != nil {
		s.fail(w, err)
		return
	}
	writeJSON(w, http.StatusOK, answer)
}

func (s *Server) submitSection(w http.ResponseWriter, r *http.Request) {
	user, ok := s.requireUser(w, r)
	if !ok {
		return
	}
	state, err := s.store.SubmitSection(r.Context(), user.ID, r.PathValue("id"), r.PathValue("skill"))
	if err != nil {
		s.fail(w, err)
		return
	}
	s.audit(r.Context(), user.ID, "section.submit", "attempt", r.PathValue("id"))
	writeJSON(w, http.StatusOK, state)
}

func (s *Server) speakingResponse(w http.ResponseWriter, r *http.Request) {
	user, ok := s.requireUser(w, r)
	if !ok {
		return
	}
	if err := r.ParseMultipartForm(16 << 20); err != nil {
		writeError(w, http.StatusBadRequest, "INVALID_UPLOAD", "Expected multipart form data")
		return
	}
	questionID := r.FormValue("questionId")
	part := atoi(r.FormValue("part"))
	duration := atoi(r.FormValue("durationSeconds"))
	transcript := r.FormValue("transcript")
	file, header, err := r.FormFile("audio")
	storageKey := ""
	if err == nil {
		defer file.Close()
		ext := strings.ToLower(filepath.Ext(header.Filename))
		if ext != ".webm" && ext != ".ogg" && ext != ".wav" && ext != ".mp4" {
			writeError(w, http.StatusBadRequest, "INVALID_AUDIO", "Unsupported audio format")
			return
		}
		dir := filepath.Join(s.mediaDir, "speaking")
		if err := os.MkdirAll(dir, 0o755); err != nil {
			s.fail(w, err)
			return
		}
		storageKey = fmt.Sprintf("%s-%s%s", r.PathValue("id"), sanitize(questionID), ext)
		dst, err := os.Create(filepath.Join(dir, storageKey))
		if err != nil {
			s.fail(w, err)
			return
		}
		defer dst.Close()
		if _, err := io.Copy(dst, io.LimitReader(file, 16<<20)); err != nil {
			s.fail(w, err)
			return
		}
	}
	if err := s.store.SaveSpeakingUpload(r.Context(), user.ID, r.PathValue("id"), questionID, part, duration, storageKey, transcript); err != nil {
		s.fail(w, err)
		return
	}
	writeJSON(w, http.StatusCreated, map[string]any{"questionId": questionID, "durationSeconds": duration, "audioUrl": func() string {
		if storageKey == "" {
			return ""
		}
		return "/media/speaking/" + storageKey
	}()})
}

func (s *Server) completeAttempt(w http.ResponseWriter, r *http.Request) {
	user, ok := s.requireUser(w, r)
	if !ok {
		return
	}
	result, err := s.store.CompleteAttempt(r.Context(), user.ID, r.PathValue("id"))
	if err != nil {
		s.fail(w, err)
		return
	}
	s.audit(r.Context(), user.ID, "attempt.complete", "attempt", r.PathValue("id"))
	writeJSON(w, http.StatusOK, result)
}

func (s *Server) getResult(w http.ResponseWriter, r *http.Request) {
	user, ok := s.requireUser(w, r)
	if !ok {
		return
	}
	result, err := s.store.GetResult(r.Context(), user.ID, r.PathValue("id"))
	if err != nil {
		s.fail(w, err)
		return
	}
	writeJSON(w, http.StatusOK, result)
}

func (s *Server) getReview(w http.ResponseWriter, r *http.Request) {
	user, ok := s.requireUser(w, r)
	if !ok {
		return
	}
	review, err := s.store.GetReview(r.Context(), user.ID, r.PathValue("id"))
	if err != nil {
		s.fail(w, err)
		return
	}
	writeJSON(w, http.StatusOK, review)
}

func (s *Server) history(w http.ResponseWriter, r *http.Request) {
	user, ok := s.requireUser(w, r)
	if !ok {
		return
	}
	items, err := s.store.History(r.Context(), user.ID)
	if err != nil {
		s.fail(w, err)
		return
	}
	writeJSON(w, http.StatusOK, map[string]any{"attempts": items})
}

func (s *Server) adminSummary(w http.ResponseWriter, r *http.Request) {
	user, ok := s.requireUser(w, r)
	if !ok {
		return
	}
	if user.Role != "administrator" && !s.demoMode {
		writeError(w, http.StatusForbidden, "FORBIDDEN", "Administrator access required")
		return
	}
	writeJSON(w, http.StatusOK, map[string]any{
		"exam": s.exams[0].Title, "examId": s.exams[0].ID, "version": s.exams[0].Version,
		"listeningQuestions": len(s.exams[0].AllListeningQuestions()), "readingQuestions": len(s.exams[0].AllReadingQuestions()),
		"writingTasks": len(s.exams[0].Writing), "speakingParts": len(s.exams[0].Speaking),
		"contentValidated": true, "evaluationProvider": "local-rubric-v1", "demoMode": s.demoMode,
	})
}

func (s *Server) me(w http.ResponseWriter, r *http.Request) {
	user, ok := s.requireUser(w, r)
	if !ok {
		return
	}
	writeJSON(w, http.StatusOK, map[string]any{"user": user, "demoMode": s.demoMode})
}

func (s *Server) register(w http.ResponseWriter, r *http.Request) {
	var body struct {
		Email       string `json:"email"`
		Password    string `json:"password"`
		DisplayName string `json:"displayName"`
	}
	if err := decode(r, &body); err != nil {
		writeError(w, http.StatusBadRequest, "INVALID_BODY", err.Error())
		return
	}
	user, err := s.store.CreateUser(r.Context(), body.Email, body.Password, body.DisplayName)
	if err != nil {
		s.fail(w, err)
		return
	}
	if err := s.issueSession(w, r, user.ID); err != nil {
		s.fail(w, err)
		return
	}
	writeJSON(w, http.StatusCreated, map[string]any{"user": user})
}

func (s *Server) login(w http.ResponseWriter, r *http.Request) {
	var body struct {
		Email    string `json:"email"`
		Password string `json:"password"`
	}
	if err := decode(r, &body); err != nil {
		writeError(w, http.StatusBadRequest, "INVALID_BODY", err.Error())
		return
	}
	user, err := s.store.Authenticate(r.Context(), body.Email, body.Password)
	if err != nil {
		writeError(w, http.StatusUnauthorized, "INVALID_CREDENTIALS", "Email or password is incorrect")
		return
	}
	if err := s.issueSession(w, r, user.ID); err != nil {
		s.fail(w, err)
		return
	}
	writeJSON(w, http.StatusOK, map[string]any{"user": user})
}

func (s *Server) logout(w http.ResponseWriter, r *http.Request) {
	if cookie, err := r.Cookie("apex_session"); err == nil {
		_ = s.store.DeleteSession(r.Context(), hashToken(cookie.Value))
	}
	http.SetCookie(w, &http.Cookie{Name: "apex_session", Value: "", Path: "/", MaxAge: -1, HttpOnly: true, SameSite: http.SameSiteLaxMode})
	writeJSON(w, http.StatusOK, map[string]any{"ok": true})
}

func (s *Server) issueSession(w http.ResponseWriter, r *http.Request, userID string) error {
	buf := make([]byte, 32)
	if _, err := rand.Read(buf); err != nil {
		return err
	}
	token := base64.RawURLEncoding.EncodeToString(buf)
	if err := s.store.CreateSession(r.Context(), userID, hashToken(token), time.Now().Add(7*24*time.Hour)); err != nil {
		return err
	}
	http.SetCookie(w, &http.Cookie{
		Name: "apex_session", Value: token, Path: "/", HttpOnly: true,
		SameSite: http.SameSiteLaxMode, Secure: os.Getenv("COOKIE_SECURE") == "true",
		MaxAge: 7 * 24 * 3600,
	})
	return nil
}

func (s *Server) requireUser(w http.ResponseWriter, r *http.Request) (model.User, bool) {
	if s.demoMode {
		user, err := s.store.DemoUser(r.Context())
		if err == nil {
			return user, true
		}
	}
	cookie, err := r.Cookie("apex_session")
	if err == nil {
		user, err := s.store.UserBySession(r.Context(), hashToken(cookie.Value))
		if err == nil {
			return user, true
		}
	}
	writeError(w, http.StatusUnauthorized, "UNAUTHENTICATED", "Sign in to continue")
	return model.User{}, false
}

func hashToken(token string) string {
	sum := sha256.Sum256([]byte(token))
	return hex.EncodeToString(sum[:])
}

func (s *Server) fail(w http.ResponseWriter, err error) {
	switch {
	case errors.Is(err, db.ErrNotFound):
		writeError(w, http.StatusNotFound, "NOT_FOUND", "Resource not found")
	case errors.Is(err, db.ErrForbidden):
		writeError(w, http.StatusForbidden, "FORBIDDEN", "You do not have access to this resource")
	case errors.Is(err, db.ErrConflict):
		writeError(w, http.StatusConflict, "CONFLICT", "The answer was changed elsewhere. Refresh and retry.")
	case errors.Is(err, db.ErrSectionClosed):
		writeError(w, http.StatusConflict, "SECTION_CLOSED", "This section is closed and can no longer be edited")
	default:
		s.logger.Error("request failed", "err", err)
		writeError(w, http.StatusInternalServerError, "INTERNAL", "An unexpected error occurred")
	}
}

func (s *Server) audit(ctx context.Context, userID, action, entity, entityID string) {
	_, _ = s.store.Pool.Exec(ctx, `INSERT INTO audit_logs (user_id,action,entity,entity_id) VALUES ($1,$2,$3,$4)`, userID, action, entity, entityID)
}

func (s *Server) cors(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		origin := r.Header.Get("Origin")
		if origin == s.webOrigin || strings.HasPrefix(origin, "http://127.0.0.1:") || strings.HasPrefix(origin, "http://localhost:") {
			w.Header().Set("Access-Control-Allow-Origin", origin)
			w.Header().Set("Access-Control-Allow-Credentials", "true")
			w.Header().Set("Vary", "Origin")
			w.Header().Set("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
			w.Header().Set("Access-Control-Allow-Headers", "Content-Type,Authorization")
		}
		if r.Method == http.MethodOptions {
			w.WriteHeader(http.StatusNoContent)
			return
		}
		next.ServeHTTP(w, r)
	})
}

func (s *Server) logging(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()
		next.ServeHTTP(w, r)
		s.logger.Info("request", "method", r.Method, "path", r.URL.Path, "duration", time.Since(start).String())
	})
}

func (s *Server) recoverer(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		defer func() {
			if recovered := recover(); recovered != nil {
				s.logger.Error("panic", "value", recovered)
				writeError(w, http.StatusInternalServerError, "INTERNAL", "An unexpected error occurred")
			}
		}()
		next.ServeHTTP(w, r)
	})
}

func decode(r *http.Request, target any) error {
	defer r.Body.Close()
	decoder := json.NewDecoder(io.LimitReader(r.Body, 1<<20))
	decoder.DisallowUnknownFields()
	return decoder.Decode(target)
}

func writeJSON(w http.ResponseWriter, status int, value any) {
	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(value)
}

func writeError(w http.ResponseWriter, status int, code, message string) {
	writeJSON(w, status, map[string]any{"error": map[string]string{"code": code, "message": message}})
}

func sanitize(value string) string {
	return strings.Map(func(r rune) rune {
		if (r >= 'a' && r <= 'z') || (r >= 'A' && r <= 'Z') || (r >= '0' && r <= '9') || r == '-' || r == '_' {
			return r
		}
		return '-'
	}, value)
}

func atoi(value string) int {
	var n int
	_, _ = fmt.Sscanf(value, "%d", &n)
	return n
}

func env(key, fallback string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return fallback
}

func LoadContentForServer() ([]model.Exam, error) {
	pack, err := content.Load()
	if err != nil {
		return nil, err
	}
	return pack.Exams, nil
}
