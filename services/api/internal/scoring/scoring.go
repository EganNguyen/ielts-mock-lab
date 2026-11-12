package scoring

import (
	"math"
	"regexp"
	"sort"
	"strings"
	"time"
	"unicode"

	"apex/api/internal/model"
)

var nonAnswer = regexp.MustCompile(`[.,!?;:'"()]`)
var spaces = regexp.MustCompile(`\s+`)
var wordPattern = regexp.MustCompile(`[A-Za-z0-9'’-]+`)
var sentenceSplit = regexp.MustCompile(`[.!?]+`)
var linkerPattern = regexp.MustCompile(`(?i)\b(however|therefore|moreover|furthermore|although|whereas|while|in contrast|on the other hand|for example|for instance|in addition|consequently|as a result|nevertheless|in conclusion|firstly|secondly|finally|such as)\b`)

func Normalize(value string) string {
	value = strings.ToLower(strings.TrimSpace(value))
	value = nonAnswer.ReplaceAllString(value, "")
	value = spaces.ReplaceAllString(value, " ")
	return value
}

func Correct(question model.Question, answer string) bool {
	if strings.TrimSpace(answer) == "" {
		return false
	}
	given := Normalize(answer)
	candidates := append([]string{question.Answer}, question.Accepted...)
	for _, candidate := range candidates {
		if Normalize(candidate) == given {
			return true
		}
		if stripArticle(Normalize(candidate)) == stripArticle(given) {
			return true
		}
	}
	return false
}

func stripArticle(value string) string {
	for _, article := range []string{"a ", "an ", "the "} {
		if strings.HasPrefix(value, article) {
			return strings.TrimPrefix(value, article)
		}
	}
	return value
}

type bandRow struct {
	min  int
	band float64
}

var listeningTable = []bandRow{{39, 9}, {37, 8.5}, {35, 8}, {32, 7.5}, {30, 7}, {26, 6.5}, {23, 6}, {18, 5.5}, {16, 5}, {13, 4.5}, {10, 4}, {6, 3.5}, {4, 3}, {3, 2.5}, {2, 2}, {1, 1.5}}
var readingTable = []bandRow{{39, 9}, {37, 8.5}, {35, 8}, {33, 7.5}, {30, 7}, {27, 6.5}, {23, 6}, {19, 5.5}, {15, 5}, {13, 4.5}, {10, 4}, {8, 3.5}, {6, 3}, {4, 2.5}, {3, 2}, {1, 1.5}}

func BandFromRaw(raw, total int, skill string) float64 {
	scaled := int(math.Round(float64(raw) / float64(total) * 40))
	table := readingTable
	if skill == "listening" {
		table = listeningTable
	}
	for _, row := range table {
		if scaled >= row.min {
			return row.band
		}
	}
	return 1
}

func Objective(questions []model.Question, answers map[string]model.Answer, skill string) model.SectionResult {
	raw := 0
	for _, question := range questions {
		if Correct(question, answers[question.ID].Value) {
			raw++
		}
	}
	return model.SectionResult{Skill: skill, Raw: raw, Total: len(questions), Band: BandFromRaw(raw, len(questions), skill), Label: "raw score conversion"}
}

func CountWords(text string) int {
	words := wordPattern.FindAllString(text, -1)
	return len(words)
}

func paragraphs(text string) []string {
	var out []string
	for _, block := range regexp.MustCompile(`\n\s*\n`).Split(text, -1) {
		if strings.TrimSpace(block) != "" {
			out = append(out, strings.TrimSpace(block))
		}
	}
	return out
}

func lexicalDiversity(text string) float64 {
	words := regexp.MustCompile(`[a-z]+`).FindAllString(strings.ToLower(text), -1)
	if len(words) < 30 {
		return 0
	}
	unique := map[string]bool{}
	for _, word := range words {
		unique[word] = true
	}
	return float64(len(unique)) / float64(len(words))
}

func sentenceStats(text string) (float64, float64) {
	parts := sentenceSplit.Split(text, -1)
	var lengths []float64
	for _, part := range parts {
		n := len(strings.Fields(part))
		if n > 2 {
			lengths = append(lengths, float64(n))
		}
	}
	if len(lengths) == 0 {
		return 0, 0
	}
	sum := 0.0
	for _, n := range lengths {
		sum += n
	}
	mean := sum / float64(len(lengths))
	variance := 0.0
	for _, n := range lengths {
		variance += (n - mean) * (n - mean)
	}
	return mean, math.Sqrt(variance / float64(len(lengths)))
}

func clamp(n float64) float64 {
	n = math.Max(4, math.Min(9, n))
	return math.Round(n*2) / 2
}

func has(pattern, text string) bool {
	return regexp.MustCompile(pattern).MatchString(text)
}

func evaluateTask1(text string) (float64, []model.Criterion) {
	words := CountWords(text)
	paras := paragraphs(text)
	lower := strings.ToLower(text)
	overview := has(`\b(overall|in general|broadly|the most striking|the main (trend|feature)|it is clear that)\b`, lower)
	comparisons := len(regexp.MustCompile(`\b(compared|whereas|while|than|higher|lower|rose|fell|increased|decreased|tripled|doubled|remained)\b`).FindAllString(lower, -1))
	figures := len(regexp.MustCompile(`\b\d+(\.\d+)?%?\b`).FindAllString(text, -1))
	div := lexicalDiversity(text)
	avg, variety := sentenceStats(text)
	linkers := len(linkerPattern.FindAllString(text, -1))
	ta, cc, lr, gra := 5.5, 4.5, 5.0, 5.0
	if words >= 150 {
		ta += 0.5
	}
	if words >= 190 {
		ta += 0.25
	}
	if overview {
		ta += 0.75
	}
	if comparisons >= 5 {
		ta += 0.5
	}
	if figures >= 5 {
		ta += 0.25
	}
	if words < 150 {
		ta -= 1
	}
	if len(paras) >= 3 {
		cc += 1
	}
	if len(paras) >= 4 {
		cc += 0.5
	}
	if linkers >= 3 {
		cc += 0.5
	}
	if linkers >= 6 {
		cc += 0.25
	}
	if div > .43 {
		lr += .75
	}
	if div > .5 {
		lr += .5
	}
	if words > 190 {
		lr += .25
	}
	if avg > 12 {
		gra += .5
	}
	if avg > 16 {
		gra += .5
	}
	if variety > 6 {
		gra += .5
	}
	if variety > 10 {
		gra += .25
	}
	return (clamp(ta) + clamp(cc) + clamp(lr) + clamp(gra)) / 4, []model.Criterion{
		{Name: "Task achievement", Score: clamp(ta), Feedback: feedback(overview, "There is a clear overview and data is selected rather than merely listed.", "Add a clear overview identifying the main trends before describing details.")},
		{Name: "Coherence & cohesion", Score: clamp(cc), Feedback: feedback(len(paras) >= 3, "The report is organised into logical paragraphs with natural linking.", "Divide the report into an introduction, overview and detail paragraphs.")},
		{Name: "Lexical resource", Score: clamp(lr), Feedback: feedback(div > .43, "Vocabulary is varied and generally precise.", "Use a wider range of verbs and nouns for change, comparison and quantity.")},
		{Name: "Grammatical range", Score: clamp(gra), Feedback: feedback(variety > 6, "Sentence structures show useful variety.", "Vary sentence length and use comparative structures.")},
	}
}

func evaluateTask2(text string) (float64, []model.Criterion) {
	words := CountWords(text)
	paras := paragraphs(text)
	lower := strings.ToLower(text)
	both := has(`\b(some (people|argue|believe)|others|on the other hand|opponents|supporters|one view|the other view)\b`, lower)
	opinion := has(`\b(i believe|i think|in my (view|opinion)|i would argue|my own view|it seems to me)\b`, lower)
	examples := has(`\b(for example|for instance|such as|a case in point)\b`, lower)
	div := lexicalDiversity(text)
	avg, variety := sentenceStats(text)
	linkers := len(linkerPattern.FindAllString(text, -1))
	ta, cc, lr, gra := 5.0, 4.5, 5.0, 5.0
	if words >= 250 {
		ta += 1
	}
	if words >= 300 {
		ta += .5
	}
	if both {
		ta += .5
	}
	if opinion {
		ta += .5
	}
	if examples {
		ta += .25
	}
	if words < 250 {
		ta -= 1.5
	}
	if len(paras) >= 4 {
		cc += 1.25
	}
	if len(paras) >= 5 {
		cc += .5
	}
	if linkers >= 4 {
		cc += .5
	}
	if linkers >= 8 {
		cc += .25
	}
	if div > .42 {
		lr += .75
	}
	if div > .48 {
		lr += .5
	}
	if words > 300 {
		lr += .25
	}
	if avg > 13 {
		gra += .5
	}
	if avg > 18 {
		gra += .5
	}
	if variety > 7 {
		gra += .5
	}
	if variety > 11 {
		gra += .25
	}
	return (clamp(ta) + clamp(cc) + clamp(lr) + clamp(gra)) / 4, []model.Criterion{
		{Name: "Task response", Score: clamp(ta), Feedback: feedback(both && opinion, "Both views are addressed and a clear personal position is maintained.", "Develop both views and keep your own position clear throughout.")},
		{Name: "Coherence & cohesion", Score: clamp(cc), Feedback: feedback(len(paras) >= 4, "Paragraphing is clear and progression of ideas is easy to follow.", "Use four or five paragraphs, each with one central idea.")},
		{Name: "Lexical resource", Score: clamp(lr), Feedback: feedback(div > .42, "There is a good range of vocabulary with some less common items.", "Replace repeated general words with precise alternatives.")},
		{Name: "Grammatical range", Score: clamp(gra), Feedback: feedback(variety > 7, "A mix of simple and complex sentences is used effectively.", "Include more complex sentences, especially concession and conditionals.")},
	}
}

func feedback(ok bool, good, improve string) string {
	if ok {
		return good
	}
	return improve
}

func EvaluateWriting(writing model.WritingResponses) model.WritingEvaluation {
	b1, c1 := evaluateTask1(writing.Task1)
	b2, c2 := evaluateTask2(writing.Task2)
	band := clamp((b1 + b2*2) / 3)
	w1, w2 := CountWords(writing.Task1), CountWords(writing.Task2)
	var notes []string
	if w1 < 150 {
		notes = append(notes, "Task 1 is below the 150-word minimum. Under-length answers lose marks for task achievement.")
	}
	if w2 < 250 {
		notes = append(notes, "Task 2 is below the 250-word minimum. Develop your argument to at least 250 words.")
	}
	if w1 >= 150 && w2 >= 250 {
		notes = append(notes, "Both tasks meet the minimum word count.")
	}
	notes = append(notes, "Indicative local evaluation using the Apex rubric v1. This is not an official IELTS score.")
	return model.WritingEvaluation{Band: band, Criteria: append(c1, c2...), Feedback: notes, Task1Words: w1, Task2Words: w2}
}

func EvaluateSpeaking(responses []model.SpeakingResponse, totalQuestions int) model.SpeakingEvaluation {
	answered := len(responses)
	seconds := 0
	words := 0
	for _, response := range responses {
		seconds += response.Duration
		words += CountWords(response.Transcript)
	}
	completion := float64(0)
	if totalQuestions > 0 {
		completion = math.Min(1, float64(answered)/float64(totalQuestions))
	}
	band := 4 + completion*2.5
	if seconds >= 120 {
		band += .25
	}
	if seconds >= 240 {
		band += .5
	}
	if seconds >= 420 {
		band += .25
	}
	if words > 0 && seconds > 0 {
		wpm := float64(words) / (float64(seconds) / 60)
		if wpm >= 100 {
			band += .25
		}
		if wpm >= 130 {
			band += .25
		}
		if wpm < 60 {
			band -= .25
		}
	}
	notes := []string{"Local completion-based estimate. Pronunciation, fluency and coherence require a trained examiner."}
	if answered < totalQuestions {
		notes = append(notes, strings.Join([]string{"Some speaking prompts were not recorded."}, ""))
	}
	notes = append(notes, "Speaking estimate uses recording completion, duration and any available transcript.")
	return model.SpeakingEvaluation{Band: clamp(band), Answered: answered, TotalQuestions: totalQuestions, TotalSeconds: seconds, Words: words, Notes: notes}
}

func BuildResult(attempt model.Attempt, exam model.Exam, answers map[string]model.Answer, writing model.WritingResponses, speaking []model.SpeakingResponse, versions model.ScoringConfig) model.Result {
	listening := Objective(exam.AllListeningQuestions(), answers, "listening")
	reading := Objective(exam.AllReadingQuestions(), answers, "reading")
	writingEval := EvaluateWriting(writing)
	speakingEval := EvaluateSpeaking(speaking, len(exam.AllSpeakingQuestions())+1)
	writingResult := model.SectionResult{Skill: "writing", Band: writingEval.Band, Label: "local rubric estimate"}
	speakingResult := model.SectionResult{Skill: "speaking", Band: speakingEval.Band, Label: "completion-based estimate"}
	overall := math.Round(((listening.Band+reading.Band+writingResult.Band+speakingResult.Band)/4)*2) / 2
	return model.Result{
		AttemptID: attempt.ID, ExamTitle: exam.Title, Mode: attempt.Mode, Listening: listening, Reading: reading,
		Writing: writingResult, Speaking: speakingResult, Overall: overall,
		CompletedAt: time.Now().UTC(), WritingEval: writingEval, SpeakingEval: speakingEval,
		Official: false, ScoringVersions: versions,
	}
}

func SortedNumbers(questions []model.Question) []int {
	out := make([]int, len(questions))
	for i, q := range questions {
		out[i] = q.Number
	}
	sort.Ints(out)
	return out
}

func IsLetter(value string) bool {
	if len(value) != 1 {
		return false
	}
	return unicode.IsLetter(rune(value[0]))
}
