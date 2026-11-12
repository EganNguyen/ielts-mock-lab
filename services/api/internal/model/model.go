package model

import "time"

type Question struct {
	ID          string   `json:"id"`
	Number      int      `json:"number"`
	GroupID     string   `json:"groupId"`
	Type        string   `json:"type"`
	Prompt      string   `json:"prompt"`
	Options     []string `json:"options,omitempty"`
	Answer      string   `json:"answer,omitempty"`
	Accepted    []string `json:"accepted,omitempty"`
	Explanation string   `json:"explanation,omitempty"`
}

type QuestionGroup struct {
	ID            string   `json:"id"`
	Label         string   `json:"label,omitempty"`
	Instructions  string   `json:"instructions"`
	RangeStart    int      `json:"-"`
	RangeEnd      int      `json:"-"`
	Range         []int    `json:"range"`
	Layout        string   `json:"layout,omitempty"`
	SharedOptions []string `json:"sharedOptions,omitempty"`
	Note          string   `json:"note,omitempty"`
	Body          []string `json:"body,omitempty"`
	Figure        string   `json:"figure,omitempty"`
	FigureAlt     string   `json:"figureAlt,omitempty"`
}

type TranscriptLine struct {
	Speaker string `json:"speaker"`
	Text    string `json:"text"`
}

type ListeningPart struct {
	ID         string           `json:"id"`
	Number     int              `json:"number"`
	Title      string           `json:"title"`
	Context    string           `json:"context"`
	Groups     []QuestionGroup  `json:"groups"`
	Questions  []Question       `json:"questions"`
	Transcript []TranscriptLine `json:"transcript,omitempty"`
}

type Paragraph struct {
	Label string `json:"label"`
	Text  string `json:"text"`
}

type ReadingPassage struct {
	ID         string          `json:"id"`
	Number     int             `json:"number"`
	Title      string          `json:"title"`
	Subtitle   string          `json:"subtitle"`
	Paragraphs []Paragraph     `json:"paragraphs"`
	Groups     []QuestionGroup `json:"groups"`
	Questions  []Question      `json:"questions"`
}

type WritingTask struct {
	ID               string   `json:"id"`
	Number           int      `json:"number"`
	Title            string   `json:"title"`
	Prompt           string   `json:"prompt"`
	Instructions     []string `json:"instructions"`
	MinimumWords     int      `json:"minimumWords"`
	SuggestedMinutes int      `json:"suggestedMinutes"`
	ModelAnswer      string   `json:"modelAnswer,omitempty"`
	ModelHighlights  []string `json:"modelHighlights,omitempty"`
	Chart            string   `json:"chart,omitempty"`
	Figure           string   `json:"figure,omitempty"`
	FigureAlt        string   `json:"figureAlt,omitempty"`
}

type SpeakingQuestion struct {
	ID       string `json:"id"`
	Text     string `json:"text"`
	FollowUp string `json:"followUp,omitempty"`
}

type CueCard struct {
	Topic              string   `json:"topic"`
	Bullets            []string `json:"bullets"`
	Rounding           string   `json:"rounding"`
	PreparationSeconds int      `json:"preparationSeconds"`
	SpeakingSeconds    int      `json:"speakingSeconds"`
}

type SpeakingPart struct {
	ID          string             `json:"id"`
	Number      int                `json:"number"`
	Title       string             `json:"title"`
	Description string             `json:"description"`
	Questions   []SpeakingQuestion `json:"questions"`
	CueCard     *CueCard           `json:"cueCard,omitempty"`
}

type ScoringConfig struct {
	ListeningVersion string `json:"listeningVersion"`
	ReadingVersion   string `json:"readingVersion"`
	RubricVersion    string `json:"rubricVersion"`
}

type Exam struct {
	ID          string           `json:"id"`
	Title       string           `json:"title"`
	Module      string           `json:"module"`
	Version     string           `json:"version"`
	Listening   []ListeningPart  `json:"listening"`
	Reading     []ReadingPassage `json:"reading"`
	Writing     []WritingTask    `json:"writing"`
	Speaking    []SpeakingPart   `json:"speaking"`
	PublishedAt string           `json:"publishedAt,omitempty"`
	Scoring     ScoringConfig    `json:"scoring"`
	AudioURL    string           `json:"audioUrl,omitempty"`
}

// Public returns a deep-enough copy of the exam with all assessment material removed.
// Answer keys, explanations, transcripts and model answers must never reach the browser
// before the attempt has been submitted.
func (e Exam) Public() Exam {
	public := e
	if public.AudioURL == "" {
		public.AudioURL = "/media/listening/" + e.ID
	}
	public.Listening = make([]ListeningPart, len(e.Listening))
	for i, part := range e.Listening {
		part.Transcript = nil
		part.Questions = publicQuestions(part.Questions)
		public.Listening[i] = part
	}
	public.Reading = make([]ReadingPassage, len(e.Reading))
	for i, passage := range e.Reading {
		passage.Questions = publicQuestions(passage.Questions)
		public.Reading[i] = passage
	}
	public.Writing = make([]WritingTask, len(e.Writing))
	for i, task := range e.Writing {
		task.ModelAnswer = ""
		task.ModelHighlights = nil
		public.Writing[i] = task
	}
	return public
}

func publicQuestions(questions []Question) []Question {
	out := make([]Question, len(questions))
	for i, question := range questions {
		question.Answer = ""
		question.Accepted = nil
		question.Explanation = ""
		out[i] = question
	}
	return out
}

func (e Exam) AllListeningQuestions() []Question {
	var out []Question
	for _, part := range e.Listening {
		out = append(out, part.Questions...)
	}
	return out
}

func (e Exam) AllReadingQuestions() []Question {
	var out []Question
	for _, passage := range e.Reading {
		out = append(out, passage.Questions...)
	}
	return out
}

func (e Exam) AllSpeakingQuestions() []SpeakingQuestion {
	var out []SpeakingQuestion
	for _, part := range e.Speaking {
		out = append(out, part.Questions...)
	}
	return out
}

type User struct {
	ID          string    `json:"id"`
	Email       string    `json:"email"`
	DisplayName string    `json:"displayName"`
	Role        string    `json:"role"`
	CreatedAt   time.Time `json:"createdAt"`
}

type SectionState struct {
	Skill            string     `json:"skill"`
	Status           string     `json:"status"`
	StartedAt        *time.Time `json:"startedAt,omitempty"`
	DeadlineAt       *time.Time `json:"deadlineAt,omitempty"`
	SubmittedAt      *time.Time `json:"submittedAt,omitempty"`
	DurationSeconds  int        `json:"durationSeconds"`
	RemainingSeconds int        `json:"remainingSeconds"`
}

type Attempt struct {
	ID           string         `json:"id"`
	ExamID       string         `json:"examId"`
	Mode         string         `json:"mode"`
	Status       string         `json:"status"`
	CurrentSkill string         `json:"currentSkill"`
	StartedAt    time.Time      `json:"startedAt"`
	CompletedAt  *time.Time     `json:"completedAt,omitempty"`
	Sections     []SectionState `json:"sections"`
}

type Answer struct {
	QuestionID string `json:"questionId"`
	Value      string `json:"value"`
	Version    int    `json:"version"`
}

type WritingResponses struct {
	Task1 string `json:"task1"`
	Task2 string `json:"task2"`
}

type SpeakingResponse struct {
	QuestionID string `json:"questionId"`
	Duration   int    `json:"durationSeconds"`
	Transcript string `json:"transcript,omitempty"`
	AudioURL   string `json:"audioUrl,omitempty"`
	Part       int    `json:"part"`
}

type AttemptState struct {
	Attempt    Attempt            `json:"attempt"`
	Exam       Exam               `json:"exam"`
	Answers    map[string]Answer  `json:"answers"`
	Writing    WritingResponses   `json:"writing"`
	Speaking   []SpeakingResponse `json:"speaking"`
	ServerTime time.Time          `json:"serverTime"`
}

type Criterion struct {
	Name     string  `json:"name"`
	Score    float64 `json:"score"`
	Feedback string  `json:"feedback"`
}

type WritingEvaluation struct {
	Band       float64     `json:"band"`
	Criteria   []Criterion `json:"criteria"`
	Feedback   []string    `json:"feedback"`
	Task1Words int         `json:"task1Words"`
	Task2Words int         `json:"task2Words"`
}

type SpeakingEvaluation struct {
	Band           float64  `json:"band"`
	Answered       int      `json:"answered"`
	TotalQuestions int      `json:"totalQuestions"`
	TotalSeconds   int      `json:"totalSeconds"`
	Words          int      `json:"words"`
	Notes          []string `json:"notes"`
}

type SectionResult struct {
	Skill string  `json:"skill"`
	Raw   int     `json:"raw"`
	Total int     `json:"total"`
	Band  float64 `json:"band"`
	Label string  `json:"label,omitempty"`
}

type Result struct {
	AttemptID       string             `json:"attemptId"`
	ExamTitle       string             `json:"examTitle,omitempty"`
	Mode            string             `json:"mode"`
	Listening       SectionResult      `json:"listening"`
	Reading         SectionResult      `json:"reading"`
	Writing         SectionResult      `json:"writing"`
	Speaking        SectionResult      `json:"speaking"`
	Overall         float64            `json:"overall"`
	CompletedAt     time.Time          `json:"completedAt"`
	WritingEval     WritingEvaluation  `json:"writingEvaluation"`
	SpeakingEval    SpeakingEvaluation `json:"speakingEvaluation"`
	Official        bool               `json:"official"`
	ScoringVersions ScoringConfig      `json:"scoringVersions"`
}
