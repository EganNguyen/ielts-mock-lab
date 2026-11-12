package content

import (
	"embed"
	"encoding/json"
	"fmt"
	"sort"

	"apex/api/internal/model"
)

//go:embed *-test*.json
var files embed.FS

type Pack struct {
	Exams []model.Exam
}

func Load() (Pack, error) {
	entries, err := files.ReadDir(".")
	if err != nil {
		return Pack{}, fmt.Errorf("list embedded exams: %w", err)
	}
	names := make([]string, 0, len(entries))
	for _, entry := range entries {
		if !entry.IsDir() {
			names = append(names, entry.Name())
		}
	}
	sort.Strings(names)
	exams := make([]model.Exam, 0, len(names))
	for _, name := range names {
		raw, err := files.ReadFile(name)
		if err != nil {
			return Pack{}, fmt.Errorf("read %s: %w", name, err)
		}
		var exam model.Exam
		if err := json.Unmarshal(raw, &exam); err != nil {
			return Pack{}, fmt.Errorf("decode %s: %w", name, err)
		}
		if err := Validate(exam); err != nil {
			return Pack{}, fmt.Errorf("%s: %w", name, err)
		}
		if exam.AudioURL == "" {
			exam.AudioURL = "/media/listening/" + exam.ID
		}
		exams = append(exams, exam)
	}
	if len(exams) == 0 {
		return Pack{}, fmt.Errorf("no embedded exams")
	}
	return Pack{Exams: exams}, nil
}

func Validate(exam model.Exam) error {
	if len(exam.Listening) != 4 {
		return fmt.Errorf("listening must have 4 parts, got %d", len(exam.Listening))
	}
	if len(exam.Reading) != 3 {
		return fmt.Errorf("reading must have 3 passages, got %d", len(exam.Reading))
	}
	if len(exam.Writing) != 2 {
		return fmt.Errorf("writing must have 2 tasks, got %d", len(exam.Writing))
	}
	if len(exam.Speaking) != 3 {
		return fmt.Errorf("speaking must have 3 parts, got %d", len(exam.Speaking))
	}
	l := len(exam.AllListeningQuestions())
	r := len(exam.AllReadingQuestions())
	if l != 40 {
		return fmt.Errorf("listening must have 40 questions, got %d", l)
	}
	if r != 40 {
		return fmt.Errorf("reading must have 40 questions, got %d", r)
	}
	for _, q := range append(exam.AllListeningQuestions(), exam.AllReadingQuestions()...) {
		if q.Answer == "" {
			return fmt.Errorf("question %s has no answer key", q.ID)
		}
	}
	return nil
}
