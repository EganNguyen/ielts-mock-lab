package scoring

import (
	"testing"

	"apex/api/internal/model"
)

func TestNormalizationAndAlternatives(t *testing.T) {
	q := model.Question{Answer: "BR8 4QT", Accepted: []string{"br84qt"}}
	for _, value := range []string{"BR8 4QT", " br8 4qt ", "BR84QT"} {
		if !Correct(q, value) {
			t.Fatalf("expected %q to be correct", value)
		}
	}
	if Correct(q, "BR8 5QT") {
		t.Fatal("incorrect postcode accepted")
	}
	if Correct(q, "") {
		t.Fatal("blank answer accepted")
	}
}

func TestBandConversion(t *testing.T) {
	cases := []struct {
		raw, total int
		skill      string
		want       float64
	}{
		{40, 40, "listening", 9},
		{39, 40, "listening", 9},
		{35, 40, "listening", 8},
		{30, 40, "listening", 7},
		{23, 40, "listening", 6},
		{16, 40, "listening", 5},
		{39, 40, "reading", 9},
		{33, 40, "reading", 7.5},
		{27, 40, "reading", 6.5},
		{19, 40, "reading", 5.5},
		{0, 40, "listening", 1},
	}
	for _, tc := range cases {
		if got := BandFromRaw(tc.raw, tc.total, tc.skill); got != tc.want {
			t.Errorf("%s %d/%d: got %.1f want %.1f", tc.skill, tc.raw, tc.total, got, tc.want)
		}
	}
}

func TestObjectiveScoring(t *testing.T) {
	questions := []model.Question{
		{ID: "q1", Answer: "Marsh"},
		{ID: "q2", Answer: "Ellison"},
		{ID: "q3", Answer: "BR8 4QT"},
	}
	answers := map[string]model.Answer{
		"q1": {Value: "marsh"}, "q2": {Value: "wrong"}, "q3": {Value: "BR8 4QT"},
	}
	result := Objective(questions, answers, "listening")
	if result.Raw != 2 || result.Total != 3 {
		t.Fatalf("expected 2/3, got %d/%d", result.Raw, result.Total)
	}
}

func TestWritingEvaluation(t *testing.T) {
	strong := model.WritingResponses{
		Task1: "Overall, the chart shows internet use rose in every age group between 2010 and 2022. In 2010, usage was 76% among 18-29 year olds, compared with 68% among 30-44 year olds, 45% among 45-59 year olds, 23% among 60-74 year olds and only 8% among those aged 75 and over. By 2022, the figures had risen to 98%, 95%, 87%, 70% and 38% respectively. The most striking change was among older adults, whose use more than tripled, while the gap between younger and older users narrowed substantially. However, a clear generational difference remained in 2022.",
		Task2: "Some people believe universities should only offer courses leading to well-paid jobs, while others argue that socially valuable subjects deserve support even when graduates earn less. In my view, both aims matter, but funding should not be determined by salary outcomes alone.\n\nThose who favour employment-focused courses make a reasonable case. Students invest time and money in a degree and expect better job prospects. Engineering, medicine and computer science provide clear career routes, and the economy needs these graduates. If universities expanded only in low-demand fields, they might produce graduates with large debts and limited options.\n\nOn the other hand, a university is not merely a training provider. History, philosophy, social work and the arts help societies understand themselves and address problems markets do not price. A social worker may earn less than a software engineer, but their contribution is substantial. If funding were tied only to salaries, these fields would shrink and society would lose something important.\n\nIn my opinion, universities should ensure every course develops transferable skills, while governments should support subjects of social value through grants and scholarships. Employment outcomes are legitimate, but they should not be the only measure of a degree.",
	}
	evaluation := EvaluateWriting(strong)
	if evaluation.Band < 5.5 {
		t.Fatalf("strong response received unexpectedly low band %.1f", evaluation.Band)
	}
	if len(evaluation.Criteria) != 8 {
		t.Fatalf("expected 8 criteria, got %d", len(evaluation.Criteria))
	}
	if evaluation.Task2Words < 190 {
		t.Fatalf("task 2 word count incorrect: %d", evaluation.Task2Words)
	}
}

func TestSpeakingEvaluation(t *testing.T) {
	responses := []model.SpeakingResponse{
		{Duration: 120, Transcript: "I enjoy living in a city because there are many opportunities to meet people and try new things."},
		{Duration: 120, Transcript: "Public spaces are important because they give residents somewhere to relax without spending money."},
		{Duration: 120, Transcript: "Technology has changed relaxation in both positive and negative ways."},
	}
	result := EvaluateSpeaking(responses, 19)
	if result.Answered != 3 || result.TotalSeconds != 360 {
		t.Fatalf("unexpected speaking metrics: %+v", result)
	}
	if result.Band < 4 || result.Band > 9 {
		t.Fatalf("band out of range: %.1f", result.Band)
	}
}
