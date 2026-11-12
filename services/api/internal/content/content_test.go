package content

import "testing"

func TestEmbeddedExamIsComplete(t *testing.T) {
	pack, err := Load()
	if err != nil {
		t.Fatal(err)
	}
	if len(pack.Exams) != 8 {
		t.Fatalf("exams = %d, want 8", len(pack.Exams))
	}
	for _, exam := range pack.Exams {
		if got := len(exam.AllListeningQuestions()); got != 40 {
			t.Fatalf("%s listening questions = %d, want 40", exam.ID, got)
		}
		if got := len(exam.AllReadingQuestions()); got != 40 {
			t.Fatalf("%s reading questions = %d, want 40", exam.ID, got)
		}
		if len(exam.Writing) != 2 || len(exam.Speaking) != 3 {
			t.Fatalf("%s writing/speaking structure is incomplete", exam.ID)
		}
	}
}

func TestPublicExamStripsAssessmentMaterial(t *testing.T) {
	pack, err := Load()
	if err != nil {
		t.Fatal(err)
	}
	for _, exam := range pack.Exams {
		public := exam.Public()
		for _, q := range public.AllListeningQuestions() {
			if q.Answer != "" || q.Explanation != "" || len(q.Accepted) > 0 {
				t.Fatalf("public listening question %s leaked assessment material", q.ID)
			}
		}
		for _, q := range public.AllReadingQuestions() {
			if q.Answer != "" || q.Explanation != "" {
				t.Fatalf("public reading question %s leaked assessment material", q.ID)
			}
		}
		for _, part := range public.Listening {
			if len(part.Transcript) > 0 {
				t.Fatalf("public listening part %s leaked transcript", part.ID)
			}
		}
		for _, task := range public.Writing {
			if task.ModelAnswer != "" {
				t.Fatalf("public writing task %s leaked model answer", task.ID)
			}
		}
	}
}
