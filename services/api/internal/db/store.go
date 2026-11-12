package db

import (
	"context"
	"crypto/sha256"
	"embed"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"sort"
	"strings"
	"time"

	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgxpool"
	"golang.org/x/crypto/bcrypt"

	"apex/api/internal/model"
	"apex/api/internal/scoring"
)

//go:embed migrations/*.sql
var migrations embed.FS

type Store struct{ Pool *pgxpool.Pool }

var ErrNotFound = errors.New("not found")
var ErrForbidden = errors.New("forbidden")
var ErrConflict = errors.New("conflict")
var ErrSectionClosed = errors.New("section is closed")

func Open(ctx context.Context, databaseURL string) (*Store, error) {
	pool, err := pgxpool.New(ctx, databaseURL)
	if err != nil {
		return nil, err
	}
	if err := pool.Ping(ctx); err != nil {
		pool.Close()
		return nil, err
	}
	return &Store{Pool: pool}, nil
}

func (s *Store) Close() { s.Pool.Close() }

func (s *Store) Migrate(ctx context.Context) error {
	entries, err := migrations.ReadDir("migrations")
	if err != nil {
		return err
	}
	names := make([]string, 0, len(entries))
	for _, entry := range entries {
		if !entry.IsDir() && strings.HasSuffix(entry.Name(), ".sql") {
			names = append(names, entry.Name())
		}
	}
	sort.Strings(names)
	for _, name := range names {
		sql, err := migrations.ReadFile("migrations/" + name)
		if err != nil {
			return err
		}
		if _, err := s.Pool.Exec(ctx, string(sql)); err != nil {
			return fmt.Errorf("migration %s: %w", name, err)
		}
	}
	return nil
}

func (s *Store) Seed(ctx context.Context, exam model.Exam) error {
	raw, err := json.Marshal(exam)
	if err != nil {
		return err
	}
	sum := sha256.Sum256(raw)
	checksum := hex.EncodeToString(sum[:])
	tx, err := s.Pool.Begin(ctx)
	if err != nil {
		return err
	}
	defer tx.Rollback(ctx)
	if _, err := tx.Exec(ctx, `INSERT INTO exams (id, code, title, module) VALUES ($1,$2,$3,$4)
		ON CONFLICT (id) DO UPDATE SET title=EXCLUDED.title, module=EXCLUDED.module`, exam.ID, exam.ID, exam.Title, exam.Module); err != nil {
		return err
	}
	versionID := exam.ID + "-v1"
	if _, err := tx.Exec(ctx, `INSERT INTO exam_versions (id, exam_id, version_label, status, content, content_checksum, configuration, published_at)
		VALUES ($1,$2,$3,'published',$4,$5,$6,now())
		ON CONFLICT (id) DO UPDATE SET content=EXCLUDED.content, content_checksum=EXCLUDED.content_checksum, status='published'`,
		versionID, exam.ID, exam.Version, raw, checksum, `{"mode":"local-demo"}`); err != nil {
		return err
	}
	demoHash, _ := bcrypt.GenerateFromPassword([]byte("demo-local-only"), bcrypt.DefaultCost)
	if _, err := tx.Exec(ctx, `INSERT INTO users (id,email,password_hash,display_name,role)
		VALUES ('00000000-0000-4000-8000-000000000001','demo@apex.local',$1,'Demo Candidate','candidate')
		ON CONFLICT (email) DO NOTHING`, string(demoHash)); err != nil {
		return err
	}
	return tx.Commit(ctx)
}

func (s *Store) DemoUser(ctx context.Context) (model.User, error) {
	var user model.User
	err := s.Pool.QueryRow(ctx, `SELECT id::text,email,display_name,role,created_at FROM users WHERE email='demo@apex.local'`).
		Scan(&user.ID, &user.Email, &user.DisplayName, &user.Role, &user.CreatedAt)
	return user, err
}

func (s *Store) ExamVersion(ctx context.Context, examID string) (string, model.Exam, error) {
	var versionID string
	var raw []byte
	err := s.Pool.QueryRow(ctx, `SELECT id, content FROM exam_versions WHERE exam_id=$1 AND status='published' ORDER BY published_at DESC LIMIT 1`, examID).Scan(&versionID, &raw)
	if err != nil {
		return "", model.Exam{}, err
	}
	var exam model.Exam
	if err := json.Unmarshal(raw, &exam); err != nil {
		return "", model.Exam{}, err
	}
	return versionID, exam, nil
}

func (s *Store) ListExams(ctx context.Context) ([]map[string]any, error) {
	rows, err := s.Pool.Query(ctx, `SELECT e.id, e.code, e.title, e.module, ev.version_label, ev.published_at, ev.content
		FROM exams e JOIN exam_versions ev ON ev.exam_id=e.id WHERE ev.status='published' ORDER BY e.created_at DESC`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var exams []map[string]any
	for rows.Next() {
		var id, code, title, module, version string
		var published time.Time
		var raw []byte
		if err := rows.Scan(&id, &code, &title, &module, &version, &published, &raw); err != nil {
			return nil, err
		}
		var exam model.Exam
		if err := json.Unmarshal(raw, &exam); err != nil {
			return nil, err
		}
		exams = append(exams, map[string]any{
			"id": id, "code": code, "title": title, "module": module, "version": version,
			"publishedAt": published, "listeningQuestions": len(exam.AllListeningQuestions()),
			"readingQuestions": len(exam.AllReadingQuestions()), "writingTasks": len(exam.Writing),
			"speakingParts": len(exam.Speaking), "durationMinutes": 164,
		})
	}
	return exams, rows.Err()
}

func (s *Store) GetExamPublic(ctx context.Context, examID string) (model.Exam, error) {
	_, exam, err := s.ExamVersion(ctx, examID)
	if err != nil {
		return model.Exam{}, err
	}
	return exam.Public(), nil
}

var skillOrder = []string{"listening", "reading", "writing", "speaking"}
var durations = map[string]int{"listening": 1800, "reading": 3600, "writing": 3600, "speaking": 900}

func (s *Store) CreateAttempt(ctx context.Context, userID, examID, mode string) (string, error) {
	if mode == "" {
		mode = "full"
	}
	validMode := mode == "full"
	for _, skill := range skillOrder {
		if mode == skill {
			validMode = true
		}
	}
	if !validMode {
		return "", fmt.Errorf("invalid mode")
	}
	versionID, _, err := s.ExamVersion(ctx, examID)
	if err != nil {
		return "", err
	}
	tx, err := s.Pool.Begin(ctx)
	if err != nil {
		return "", err
	}
	defer tx.Rollback(ctx)
	var attemptID string
	if err := tx.QueryRow(ctx, `INSERT INTO attempts (user_id,exam_version_id,mode,status,current_skill,started_at)
		VALUES ($1,$2,$3,'in_progress',$4,now()) RETURNING id::text`, userID, versionID, mode, firstSkill(mode)).Scan(&attemptID); err != nil {
		return "", err
	}
	skills := []string{mode}
	if mode == "full" {
		skills = skillOrder
	}
	for _, skill := range skills {
		if _, err := tx.Exec(ctx, `INSERT INTO attempt_sections (attempt_id,skill,duration_seconds) VALUES ($1,$2,$3)`, attemptID, skill, durations[skill]); err != nil {
			return "", err
		}
	}
	return attemptID, tx.Commit(ctx)
}

func firstSkill(mode string) string {
	if mode == "full" {
		return "listening"
	}
	return mode
}

func (s *Store) currentSkillAllowed(mode, skill string) bool {
	return mode == "full" || mode == skill
}

func (s *Store) StartSection(ctx context.Context, userID, attemptID, skill string) error {
	attempt, err := s.getAttempt(ctx, userID, attemptID)
	if err != nil {
		return err
	}
	if !s.currentSkillAllowed(attempt.Mode, skill) {
		return ErrForbidden
	}
	if attempt.Status == "completed" {
		return ErrSectionClosed
	}
	tx, err := s.Pool.Begin(ctx)
	if err != nil {
		return err
	}
	defer tx.Rollback(ctx)
	var status string
	var deadline *time.Time
	err = tx.QueryRow(ctx, `SELECT status,deadline_at FROM attempt_sections WHERE attempt_id=$1 AND skill=$2`, attemptID, skill).Scan(&status, &deadline)
	if err != nil {
		return ErrNotFound
	}
	if status == "submitted" || status == "expired" {
		return ErrSectionClosed
	}
	if status == "not_started" {
		if attempt.Mode == "full" {
			idx := indexOf(skillOrder, skill)
			if idx > 0 {
				var previous string
				err := tx.QueryRow(ctx, `SELECT status FROM attempt_sections WHERE attempt_id=$1 AND skill=$2`, attemptID, skillOrder[idx-1]).Scan(&previous)
				if err != nil {
					return err
				}
				if previous != "submitted" && previous != "expired" {
					return fmt.Errorf("previous section is not complete")
				}
			}
		}
		if _, err := tx.Exec(ctx, `UPDATE attempt_sections SET status='in_progress',started_at=now(),deadline_at=now()+make_interval(secs => $3) WHERE attempt_id=$1 AND skill=$2`, attemptID, skill, durations[skill]); err != nil {
			return err
		}
	}
	if _, err := tx.Exec(ctx, `UPDATE attempts SET current_skill=$2,status='in_progress',updated_at=now() WHERE id=$1`, attemptID, skill); err != nil {
		return err
	}
	return tx.Commit(ctx)
}

func (s *Store) getAttempt(ctx context.Context, userID, attemptID string) (model.Attempt, error) {
	var attempt model.Attempt
	err := s.Pool.QueryRow(ctx, `SELECT id::text,exam_version_id,mode,status,current_skill,started_at,completed_at
		FROM attempts WHERE id=$1 AND user_id=$2`, attemptID, userID).
		Scan(&attempt.ID, &attempt.ExamID, &attempt.Mode, &attempt.Status, &attempt.CurrentSkill, &attempt.StartedAt, &attempt.CompletedAt)
	if errors.Is(err, pgx.ErrNoRows) {
		return attempt, ErrNotFound
	}
	return attempt, err
}

func (s *Store) GetState(ctx context.Context, userID, attemptID string) (model.AttemptState, error) {
	attempt, err := s.getAttempt(ctx, userID, attemptID)
	if err != nil {
		return model.AttemptState{}, err
	}
	if err := s.expireSections(ctx, attemptID); err != nil {
		return model.AttemptState{}, err
	}
	sections, err := s.sections(ctx, attemptID)
	if err != nil {
		return model.AttemptState{}, err
	}
	attempt.Sections = sections
	_, exam, err := s.ExamVersion(ctx, examIDFromVersion(attempt.ExamID))
	if err != nil {
		return model.AttemptState{}, err
	}
	answers, err := s.answers(ctx, attemptID)
	if err != nil {
		return model.AttemptState{}, err
	}
	speaking, err := s.speakingResponses(ctx, attemptID)
	if err != nil {
		return model.AttemptState{}, err
	}
	writing := model.WritingResponses{}
	if a, ok := answers["writing-task-1"]; ok {
		writing.Task1 = a.Value
	}
	if a, ok := answers["writing-task-2"]; ok {
		writing.Task2 = a.Value
	}
	return model.AttemptState{
		Attempt: attempt, Exam: exam.Public(), Answers: answers, Writing: writing,
		Speaking: speaking, ServerTime: time.Now().UTC(),
	}, nil
}

func examIDFromVersion(versionID string) string {
	if idx := strings.LastIndex(versionID, "-v"); idx > 0 {
		return versionID[:idx]
	}
	return versionID
}

func (s *Store) expireSections(ctx context.Context, attemptID string) error {
	_, err := s.Pool.Exec(ctx, `UPDATE attempt_sections SET status='expired',submitted_at=COALESCE(submitted_at,deadline_at)
		WHERE attempt_id=$1 AND status='in_progress' AND deadline_at < now()`, attemptID)
	return err
}

func (s *Store) sections(ctx context.Context, attemptID string) ([]model.SectionState, error) {
	rows, err := s.Pool.Query(ctx, `SELECT skill,status,started_at,deadline_at,submitted_at,duration_seconds
		FROM attempt_sections WHERE attempt_id=$1 ORDER BY array_position(ARRAY['listening','reading','writing','speaking'],skill)`, attemptID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var out []model.SectionState
	now := time.Now()
	for rows.Next() {
		var sec model.SectionState
		if err := rows.Scan(&sec.Skill, &sec.Status, &sec.StartedAt, &sec.DeadlineAt, &sec.SubmittedAt, &sec.DurationSeconds); err != nil {
			return nil, err
		}
		if sec.DeadlineAt != nil && (sec.Status == "in_progress" || sec.Status == "expired") {
			sec.RemainingSeconds = max(0, int(sec.DeadlineAt.Sub(now).Seconds()))
		} else if sec.Status == "not_started" {
			sec.RemainingSeconds = sec.DurationSeconds
		}
		out = append(out, sec)
	}
	return out, rows.Err()
}

func (s *Store) answers(ctx context.Context, attemptID string) (map[string]model.Answer, error) {
	rows, err := s.Pool.Query(ctx, `SELECT question_id,answer,version FROM answers WHERE attempt_id=$1`, attemptID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	out := map[string]model.Answer{}
	for rows.Next() {
		var a model.Answer
		if err := rows.Scan(&a.QuestionID, &a.Value, &a.Version); err != nil {
			return nil, err
		}
		out[a.QuestionID] = a
	}
	return out, rows.Err()
}

func (s *Store) speakingResponses(ctx context.Context, attemptID string) ([]model.SpeakingResponse, error) {
	rows, err := s.Pool.Query(ctx, `SELECT question_id,part_number,duration_seconds,transcript,storage_key FROM speaking_recordings WHERE attempt_id=$1 ORDER BY created_at`, attemptID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	out := []model.SpeakingResponse{}
	for rows.Next() {
		var response model.SpeakingResponse
		var key string
		if err := rows.Scan(&response.QuestionID, &response.Part, &response.Duration, &response.Transcript, &key); err != nil {
			return nil, err
		}
		if key != "" {
			response.AudioURL = "/media/speaking/" + key
		}
		out = append(out, response)
	}
	return out, rows.Err()
}

func (s *Store) SaveAnswer(ctx context.Context, userID, attemptID, skill, questionID, value string, version int) (model.Answer, error) {
	attempt, err := s.getAttempt(ctx, userID, attemptID)
	if err != nil {
		return model.Answer{}, err
	}
	if !s.currentSkillAllowed(attempt.Mode, skill) {
		return model.Answer{}, ErrForbidden
	}
	if err := s.expireSections(ctx, attemptID); err != nil {
		return model.Answer{}, err
	}
	var status string
	err = s.Pool.QueryRow(ctx, `SELECT status FROM attempt_sections WHERE attempt_id=$1 AND skill=$2`, attemptID, skill).Scan(&status)
	if err != nil {
		return model.Answer{}, ErrNotFound
	}
	if status != "in_progress" {
		return model.Answer{}, ErrSectionClosed
	}
	if !validQuestion(questionID) {
		return model.Answer{}, fmt.Errorf("unknown question")
	}
	tx, err := s.Pool.Begin(ctx)
	if err != nil {
		return model.Answer{}, err
	}
	defer tx.Rollback(ctx)
	var current int
	err = tx.QueryRow(ctx, `SELECT version FROM answers WHERE attempt_id=$1 AND question_id=$2 FOR UPDATE`, attemptID, questionID).Scan(&current)
	if errors.Is(err, pgx.ErrNoRows) {
		current = 0
	} else if err != nil {
		return model.Answer{}, err
	}
	if version != 0 && current != 0 && version != current {
		return model.Answer{}, ErrConflict
	}
	next := current + 1
	if current == 0 {
		_, err = tx.Exec(ctx, `INSERT INTO answers (attempt_id,skill,question_id,answer,version) VALUES ($1,$2,$3,$4,1)`, attemptID, skill, questionID, value)
	} else {
		_, err = tx.Exec(ctx, `UPDATE answers SET answer=$3,version=$4,saved_at=now() WHERE attempt_id=$1 AND question_id=$2`, attemptID, questionID, value, next)
	}
	if err != nil {
		return model.Answer{}, err
	}
	if err := tx.Commit(ctx); err != nil {
		return model.Answer{}, err
	}
	return model.Answer{QuestionID: questionID, Value: value, Version: next}, nil
}

func validQuestion(id string) bool {
	if id == "writing-task-1" || id == "writing-task-2" {
		return true
	}
	return strings.HasPrefix(id, "l") || strings.HasPrefix(id, "r")
}

func (s *Store) SubmitSection(ctx context.Context, userID, attemptID, skill string) (model.AttemptState, error) {
	attempt, err := s.getAttempt(ctx, userID, attemptID)
	if err != nil {
		return model.AttemptState{}, err
	}
	if !s.currentSkillAllowed(attempt.Mode, skill) {
		return model.AttemptState{}, ErrForbidden
	}
	if err := s.expireSections(ctx, attemptID); err != nil {
		return model.AttemptState{}, err
	}
	answers, err := s.answers(ctx, attemptID)
	if err != nil {
		return model.AttemptState{}, err
	}
	relevant := map[string]model.Answer{}
	for id, answer := range answers {
		if (skill == "writing" && strings.HasPrefix(id, "writing-")) || (skill == "listening" && strings.HasPrefix(id, "l")) || (skill == "reading" && strings.HasPrefix(id, "r")) {
			relevant[id] = answer
		}
	}
	snapshot, _ := json.Marshal(map[string]any{"skill": skill, "answers": relevant, "savedAt": time.Now().UTC()})
	sum := sha256.Sum256(snapshot)
	tx, err := s.Pool.Begin(ctx)
	if err != nil {
		return model.AttemptState{}, err
	}
	defer tx.Rollback(ctx)
	var status string
	err = tx.QueryRow(ctx, `SELECT status FROM attempt_sections WHERE attempt_id=$1 AND skill=$2 FOR UPDATE`, attemptID, skill).Scan(&status)
	if err != nil {
		return model.AttemptState{}, ErrNotFound
	}
	if status == "in_progress" || status == "expired" {
		if _, err := tx.Exec(ctx, `UPDATE attempt_sections SET status='submitted',submitted_at=now() WHERE attempt_id=$1 AND skill=$2`, attemptID, skill); err != nil {
			return model.AttemptState{}, err
		}
	}
	if _, err := tx.Exec(ctx, `INSERT INTO section_submissions (attempt_id,skill,snapshot,content_checksum) VALUES ($1,$2,$3,$4)
		ON CONFLICT (attempt_id,skill) DO NOTHING`, attemptID, skill, snapshot, hex.EncodeToString(sum[:])); err != nil {
		return model.AttemptState{}, err
	}
	mode := attempt.Mode
	if mode == "full" {
		idx := indexOf(skillOrder, skill)
		if idx < len(skillOrder)-1 {
			next := skillOrder[idx+1]
			if _, err := tx.Exec(ctx, `UPDATE attempts SET current_skill=$2,updated_at=now() WHERE id=$1`, attemptID, next); err != nil {
				return model.AttemptState{}, err
			}
		} else {
			if _, err := tx.Exec(ctx, `UPDATE attempts SET status='core_submitted',updated_at=now() WHERE id=$1`, attemptID); err != nil {
				return model.AttemptState{}, err
			}
		}
	} else {
		if _, err := tx.Exec(ctx, `UPDATE attempts SET status='core_submitted',updated_at=now() WHERE id=$1`, attemptID); err != nil {
			return model.AttemptState{}, err
		}
	}
	if err := tx.Commit(ctx); err != nil {
		return model.AttemptState{}, err
	}
	return s.GetState(ctx, userID, attemptID)
}

func indexOf(items []string, value string) int {
	for i, item := range items {
		if item == value {
			return i
		}
	}
	return -1
}

func (s *Store) AddSpeakingResponse(ctx context.Context, userID, attemptID string, response model.SpeakingResponse) error {
	if _, err := s.getAttempt(ctx, userID, attemptID); err != nil {
		return err
	}
	_, err := s.Pool.Exec(ctx, `INSERT INTO speaking_recordings (attempt_id,part_number,question_id,storage_key,duration_seconds,transcript)
		VALUES ($1,$2,$3,$4,$5,$6) ON CONFLICT (attempt_id,question_id) DO UPDATE SET duration_seconds=EXCLUDED.duration_seconds,transcript=EXCLUDED.transcript,storage_key=EXCLUDED.storage_key`,
		attemptID, response.Part, response.QuestionID, strings.TrimPrefix(response.AudioURL, "/media/speaking/"), response.Duration, response.Transcript)
	return err
}

func (s *Store) CompleteAttempt(ctx context.Context, userID, attemptID string) (model.Result, error) {
	attempt, err := s.getAttempt(ctx, userID, attemptID)
	if err != nil {
		return model.Result{}, err
	}
	if attempt.Status == "completed" {
		return s.GetResult(ctx, userID, attemptID)
	}
	var existing []byte
	err = s.Pool.QueryRow(ctx, `SELECT details FROM results WHERE attempt_id=$1`, attemptID).Scan(&existing)
	if err == nil {
		var result model.Result
		if err := json.Unmarshal(existing, &result); err != nil {
			return model.Result{}, err
		}
		return result, nil
	}
	if err := s.expireSections(ctx, attemptID); err != nil {
		return model.Result{}, err
	}
	_, exam, err := s.ExamVersion(ctx, examIDFromVersion(attempt.ExamID))
	if err != nil {
		return model.Result{}, err
	}
	answers, err := s.answers(ctx, attemptID)
	if err != nil {
		return model.Result{}, err
	}
	writing := model.WritingResponses{}
	if answer, ok := answers["writing-task-1"]; ok {
		writing.Task1 = answer.Value
	}
	if answer, ok := answers["writing-task-2"]; ok {
		writing.Task2 = answer.Value
	}
	speaking, err := s.speakingResponses(ctx, attemptID)
	if err != nil {
		return model.Result{}, err
	}
	result := scoring.BuildResult(attempt, exam, answers, writing, speaking, exam.Scoring)
	raw, err := json.Marshal(result)
	if err != nil {
		return model.Result{}, err
	}
	tx, err := s.Pool.Begin(ctx)
	if err != nil {
		return model.Result{}, err
	}
	defer tx.Rollback(ctx)
	if _, err := tx.Exec(ctx, `INSERT INTO results
		(attempt_id,listening_band,reading_band,writing_band,speaking_band,overall_band,details,rubric_version)
		VALUES ($1,$2,$3,$4,$5,$6,$7,$8) ON CONFLICT (attempt_id) DO NOTHING`,
		attemptID, result.Listening.Band, result.Reading.Band, result.Writing.Band, result.Speaking.Band, result.Overall, raw, exam.Scoring.RubricVersion); err != nil {
		return model.Result{}, err
	}
	if _, err := tx.Exec(ctx, `UPDATE attempts SET status='completed',completed_at=now(),updated_at=now() WHERE id=$1`, attemptID); err != nil {
		return model.Result{}, err
	}
	if _, err := tx.Exec(ctx, `UPDATE attempt_sections SET status='submitted',submitted_at=COALESCE(submitted_at,now()) WHERE attempt_id=$1 AND status IN ('in_progress','not_started')`, attemptID); err != nil {
		return model.Result{}, err
	}
	if err := tx.Commit(ctx); err != nil {
		return model.Result{}, err
	}
	return result, nil
}

func (s *Store) GetResult(ctx context.Context, userID, attemptID string) (model.Result, error) {
	if _, err := s.getAttempt(ctx, userID, attemptID); err != nil {
		return model.Result{}, err
	}
	var raw []byte
	err := s.Pool.QueryRow(ctx, `SELECT details FROM results WHERE attempt_id=$1`, attemptID).Scan(&raw)
	if errors.Is(err, pgx.ErrNoRows) {
		return model.Result{}, ErrNotFound
	}
	if err != nil {
		return model.Result{}, err
	}
	var result model.Result
	if err := json.Unmarshal(raw, &result); err != nil {
		return model.Result{}, err
	}
	return result, nil
}

type Review struct {
	Attempt  model.Attempt            `json:"attempt"`
	Exam     model.Exam               `json:"exam"`
	Answers  map[string]model.Answer  `json:"answers"`
	Writing  model.WritingResponses   `json:"writing"`
	Speaking []model.SpeakingResponse `json:"speaking"`
	Result   model.Result             `json:"result"`
}

func (s *Store) GetReview(ctx context.Context, userID, attemptID string) (Review, error) {
	attempt, err := s.getAttempt(ctx, userID, attemptID)
	if err != nil {
		return Review{}, err
	}
	if attempt.Status != "completed" {
		return Review{}, ErrForbidden
	}
	_, exam, err := s.ExamVersion(ctx, examIDFromVersion(attempt.ExamID))
	if err != nil {
		return Review{}, err
	}
	answers, err := s.answers(ctx, attemptID)
	if err != nil {
		return Review{}, err
	}
	writing := model.WritingResponses{}
	if answer, ok := answers["writing-task-1"]; ok {
		writing.Task1 = answer.Value
	}
	if answer, ok := answers["writing-task-2"]; ok {
		writing.Task2 = answer.Value
	}
	speaking, err := s.speakingResponses(ctx, attemptID)
	if err != nil {
		return Review{}, err
	}
	result, err := s.GetResult(ctx, userID, attemptID)
	if err != nil {
		return Review{}, err
	}
	return Review{Attempt: attempt, Exam: exam, Answers: answers, Writing: writing, Speaking: speaking, Result: result}, nil
}

func (s *Store) History(ctx context.Context, userID string) ([]map[string]any, error) {
	rows, err := s.Pool.Query(ctx, `SELECT a.id::text,a.mode,a.started_at,a.completed_at,r.overall_band,r.listening_band,r.reading_band,r.writing_band,r.speaking_band
		FROM attempts a JOIN results r ON r.attempt_id=a.id WHERE a.user_id=$1 AND a.status='completed' ORDER BY a.completed_at DESC LIMIT 20`, userID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	out := []map[string]any{}
	for rows.Next() {
		var id, mode string
		var started time.Time
		var completed *time.Time
		var overall, l, r, w, sp float64
		if err := rows.Scan(&id, &mode, &started, &completed, &overall, &l, &r, &w, &sp); err != nil {
			return nil, err
		}
		out = append(out, map[string]any{"id": id, "mode": mode, "startedAt": started, "completedAt": completed, "overall": overall, "listening": l, "reading": r, "writing": w, "speaking": sp})
	}
	return out, rows.Err()
}

func (s *Store) SaveSpeakingUpload(ctx context.Context, userID, attemptID, questionID string, part, duration int, storageKey, transcript string) error {
	if _, err := s.getAttempt(ctx, userID, attemptID); err != nil {
		return err
	}
	_, err := s.Pool.Exec(ctx, `INSERT INTO speaking_recordings (attempt_id,part_number,question_id,storage_key,duration_seconds,transcript)
		VALUES ($1,$2,$3,$4,$5,$6) ON CONFLICT (attempt_id,question_id) DO UPDATE SET duration_seconds=EXCLUDED.duration_seconds,transcript=EXCLUDED.transcript,storage_key=EXCLUDED.storage_key`,
		attemptID, part, questionID, storageKey, duration, transcript)
	return err
}

func (s *Store) CreateUser(ctx context.Context, email, password, displayName string) (model.User, error) {
	email = strings.ToLower(strings.TrimSpace(email))
	if !strings.Contains(email, "@") || len(password) < 8 {
		return model.User{}, fmt.Errorf("invalid email or password")
	}
	hash, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
	if err != nil {
		return model.User{}, err
	}
	var user model.User
	err = s.Pool.QueryRow(ctx, `INSERT INTO users (email,password_hash,display_name,role) VALUES ($1,$2,$3,'candidate')
		RETURNING id::text,email,display_name,role,created_at`, email, string(hash), displayName).Scan(&user.ID, &user.Email, &user.DisplayName, &user.Role, &user.CreatedAt)
	if err != nil {
		return model.User{}, err
	}
	return user, nil
}

func (s *Store) Authenticate(ctx context.Context, email, password string) (model.User, error) {
	var user model.User
	var hash string
	err := s.Pool.QueryRow(ctx, `SELECT id::text,email,password_hash,display_name,role,created_at FROM users WHERE email=$1`, strings.ToLower(strings.TrimSpace(email))).
		Scan(&user.ID, &user.Email, &hash, &user.DisplayName, &user.Role, &user.CreatedAt)
	if errors.Is(err, pgx.ErrNoRows) {
		return user, ErrNotFound
	}
	if err != nil {
		return user, err
	}
	if bcrypt.CompareHashAndPassword([]byte(hash), []byte(password)) != nil {
		return user, ErrForbidden
	}
	return user, nil
}

func (s *Store) CreateSession(ctx context.Context, userID, tokenHash string, expires time.Time) error {
	_, err := s.Pool.Exec(ctx, `INSERT INTO sessions (user_id,token_hash,expires_at) VALUES ($1,$2,$3)`, userID, tokenHash, expires)
	return err
}

func (s *Store) UserBySession(ctx context.Context, tokenHash string) (model.User, error) {
	var user model.User
	err := s.Pool.QueryRow(ctx, `SELECT u.id::text,u.email,u.display_name,u.role,u.created_at
		FROM sessions s JOIN users u ON u.id=s.user_id WHERE s.token_hash=$1 AND s.expires_at>now()`, tokenHash).
		Scan(&user.ID, &user.Email, &user.DisplayName, &user.Role, &user.CreatedAt)
	if errors.Is(err, pgx.ErrNoRows) {
		return user, ErrNotFound
	}
	return user, err
}

func (s *Store) DeleteSession(ctx context.Context, tokenHash string) error {
	_, err := s.Pool.Exec(ctx, `DELETE FROM sessions WHERE token_hash=$1`, tokenHash)
	return err
}

func (s *Store) ActiveAttempt(ctx context.Context, userID string) (map[string]any, error) {
	var id, mode, currentSkill, title, status string
	var started time.Time
	err := s.Pool.QueryRow(ctx, `SELECT a.id::text,a.mode,a.current_skill,COALESCE(e.title,''),a.status,a.started_at
		FROM attempts a JOIN exam_versions ev ON ev.id=a.exam_version_id JOIN exams e ON e.id=ev.exam_id
		WHERE a.user_id=$1 AND a.status IN ('ready','in_progress','core_submitted')
		ORDER BY a.created_at DESC LIMIT 1`, userID).Scan(&id, &mode, &currentSkill, &title, &status, &started)
	if errors.Is(err, pgx.ErrNoRows) {
		return nil, nil
	}
	if err != nil {
		return nil, err
	}
	return map[string]any{"id": id, "mode": mode, "currentSkill": currentSkill, "title": title, "status": status, "startedAt": started}, nil
}
