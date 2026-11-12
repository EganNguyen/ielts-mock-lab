import type {
  AnswerMap,
  Attempt,
  AttemptResult,
  Question,
  SectionResult,
  SpeakingEvaluation,
  TestData,
  WritingAnswers,
  WritingEvaluation,
} from './types'

export function normalize(value: string): string {
  return value
    .toLowerCase()
    .trim()
    .replace(/[.,!?;:'"()]/g, '')
    .replace(/\s+/g, ' ')
}

export function isCorrect(question: Question, answer: string | undefined): boolean {
  if (!answer) return false
  const candidates = [question.answer, ...(question.accepted ?? [])].map(normalize)
  const given = normalize(answer)
  if (!given) return false
  if (candidates.includes(given)) return true
  // Accept an answer with a leading article where the key does not require it.
  const stripped = given.replace(/^(a|an|the) /, '')
  return candidates.some((candidate) => candidate.replace(/^(a|an|the) /, '') === stripped)
}

export function bandFromRaw(raw: number, total: number, skill: 'listening' | 'reading'): number {
  const scaled = Math.round((raw / total) * 40)
  const table = skill === 'listening' ? listeningBands : readingBands
  for (const row of table) {
    if (scaled >= row.min) return row.band
  }
  return 1
}

const listeningBands = [
  { min: 39, band: 9 }, { min: 37, band: 8.5 }, { min: 35, band: 8 },
  { min: 32, band: 7.5 }, { min: 30, band: 7 }, { min: 26, band: 6.5 },
  { min: 23, band: 6 }, { min: 18, band: 5.5 }, { min: 16, band: 5 },
  { min: 13, band: 4.5 }, { min: 10, band: 4 }, { min: 6, band: 3.5 },
  { min: 4, band: 3 }, { min: 3, band: 2.5 }, { min: 2, band: 2 }, { min: 1, band: 1.5 },
]

const readingBands = [
  { min: 39, band: 9 }, { min: 37, band: 8.5 }, { min: 35, band: 8 },
  { min: 33, band: 7.5 }, { min: 30, band: 7 }, { min: 27, band: 6.5 },
  { min: 23, band: 6 }, { min: 19, band: 5.5 }, { min: 15, band: 5 },
  { min: 13, band: 4.5 }, { min: 10, band: 4 }, { min: 8, band: 3.5 },
  { min: 6, band: 3 }, { min: 4, band: 2.5 }, { min: 3, band: 2 }, { min: 1, band: 1.5 },
]

export function scoreObjective(
  questions: Question[],
  answers: AnswerMap,
  skill: 'listening' | 'reading',
): SectionResult {
  const raw = questions.filter((question) => isCorrect(question, answers[question.id])).length
  return {
    skill,
    raw,
    total: questions.length,
    band: bandFromRaw(raw, questions.length, skill),
    label: `${raw} / ${questions.length} correct`,
  }
}

function countWords(text: string): number {
  return text.trim() ? text.trim().split(/\s+/).filter((word) => /[A-Za-z0-9’'-]/.test(word)).length : 0
}

function paragraphs(text: string): string[] {
  return text.split(/\n\s*\n/).map((p) => p.trim()).filter(Boolean)
}

function lexicalDiversity(text: string): number {
  const words = text.toLowerCase().match(/[a-z]+/g) ?? []
  if (words.length < 30) return 0
  return new Set(words).size / words.length
}

function sentenceStats(text: string) {
  const sentences = text.split(/[.!?]+/).map((s) => s.trim()).filter((s) => s.split(/\s+/).length > 2)
  if (!sentences.length) return { average: 0, variety: 0 }
  const lengths = sentences.map((s) => s.split(/\s+/).length)
  const average = lengths.reduce((a, b) => a + b, 0) / lengths.length
  const variance = lengths.reduce((sum, n) => sum + (n - average) ** 2, 0) / lengths.length
  return { average, variety: Math.sqrt(variance) }
}

function countLinkers(text: string): number {
  const matches = text.match(/\b(however|therefore|moreover|furthermore|although|whereas|while|in contrast|on the other hand|for example|for instance|in addition|consequently|as a result|nevertheless|in conclusion|firstly|secondly|finally|such as)\b/gi)
  return matches?.length ?? 0
}

const clampBand = (n: number) => Math.max(4, Math.min(9, Math.round(n * 2) / 2))

function evaluateTask1(text: string, minimumWords: number) {
  const words = countWords(text)
  const paras = paragraphs(text)
  const lower = text.toLowerCase()
  const hasOverview = /\b(overall|in general|broadly|the most striking|the main (trend|feature)|it is clear that)\b/.test(lower)
  const comparisons = (lower.match(/\b(compared|whereas|while|than|higher|lower|rose|fell|increased|decreased|tripled|doubled|remained)\b/g) ?? []).length
  const figures = (text.match(/\b\d+(\.\d+)?%?\b/g) ?? []).length
  const diversity = lexicalDiversity(text)
  const sentences = sentenceStats(text)
  const linkers = countLinkers(text)

  let ta = 5.5
  if (words >= minimumWords) ta += 0.5
  if (words >= minimumWords + 40) ta += 0.25
  if (hasOverview) ta += 0.75
  if (comparisons >= 5) ta += 0.5
  if (figures >= 5) ta += 0.25
  if (words < minimumWords) ta -= 1

  let cc = 4.5
  if (paras.length >= 3) cc += 1
  if (paras.length >= 4) cc += 0.5
  if (linkers >= 3) cc += 0.5
  if (linkers >= 6) cc += 0.25

  let lr = 5
  if (diversity > 0.43) lr += 0.75
  if (diversity > 0.5) lr += 0.5
  if (words > 190) lr += 0.25

  let gra = 5
  if (sentences.average > 12) gra += 0.5
  if (sentences.average > 16) gra += 0.5
  if (sentences.variety > 6) gra += 0.5
  if (sentences.variety > 10) gra += 0.25

  return {
    band: (clampBand(ta) + clampBand(cc) + clampBand(lr) + clampBand(gra)) / 4,
    criteria: [
      { name: 'Task achievement', score: clampBand(ta), feedback: hasOverview ? 'There is a clear overview, and key figures are selected rather than merely listed.' : 'Add a clear overview sentence identifying the main trends before describing details.' },
      { name: 'Coherence & cohesion', score: clampBand(cc), feedback: paras.length >= 3 ? 'The report is organised into logical paragraphs with mostly natural linking.' : 'Divide the report into an introduction, overview and detail paragraphs.' },
      { name: 'Lexical resource', score: clampBand(lr), feedback: diversity > 0.43 ? 'Vocabulary is varied and generally precise.' : 'Use a wider range of verbs and nouns for change, comparison and quantity.' },
      { name: 'Grammatical range', score: clampBand(gra), feedback: sentences.variety > 6 ? 'Sentence structures show useful variety.' : 'Vary sentence length and use complex comparative structures.' },
    ],
  }
}

function evaluateTask2(text: string, minimumWords: number) {
  const words = countWords(text)
  const paras = paragraphs(text)
  const lower = text.toLowerCase()
  const hasBothViews = /\b(some (people|argue|believe)|others|on the other hand|opponents|supporters|one view|the other view)\b/.test(lower)
  const hasOpinion = /\b(i believe|i think|in my (view|opinion)|i would argue|my own view|it seems to me)\b/.test(lower)
  const hasExamples = /\b(for example|for instance|such as|a case in point)\b/.test(lower)
  const diversity = lexicalDiversity(text)
  const sentences = sentenceStats(text)
  const linkers = countLinkers(text)

  let ta = 5
  if (words >= minimumWords) ta += 1
  if (words >= minimumWords + 50) ta += 0.5
  if (hasBothViews) ta += 0.5
  if (hasOpinion) ta += 0.5
  if (hasExamples) ta += 0.25
  if (words < minimumWords) ta -= 1.5

  let cc = 4.5
  if (paras.length >= 4) cc += 1.25
  if (paras.length >= 5) cc += 0.5
  if (linkers >= 4) cc += 0.5
  if (linkers >= 8) cc += 0.25

  let lr = 5
  if (diversity > 0.42) lr += 0.75
  if (diversity > 0.48) lr += 0.5
  if (words > 300) lr += 0.25

  let gra = 5
  if (sentences.average > 13) gra += 0.5
  if (sentences.average > 18) gra += 0.5
  if (sentences.variety > 7) gra += 0.5
  if (sentences.variety > 11) gra += 0.25

  return {
    band: (clampBand(ta) + clampBand(cc) + clampBand(lr) + clampBand(gra)) / 4,
    criteria: [
      { name: 'Task response', score: clampBand(ta), feedback: hasBothViews && hasOpinion ? 'Both views are addressed and a clear personal position is maintained.' : 'Make sure both views are developed and your own position is clear throughout.' },
      { name: 'Coherence & cohesion', score: clampBand(cc), feedback: paras.length >= 4 ? 'Paragraphing is clear and progression of ideas is easy to follow.' : 'Use four or five paragraphs, each with one central idea.' },
      { name: 'Lexical resource', score: clampBand(lr), feedback: diversity > 0.42 ? 'There is a good range of vocabulary with some less common items.' : 'Replace repeated general words with more precise alternatives.' },
      { name: 'Grammatical range', score: clampBand(gra), feedback: sentences.variety > 7 ? 'A mix of simple and complex sentences is used effectively.' : 'Include more complex sentences, especially concession and conditionals.' },
    ],
  }
}

export function evaluateWriting(writing: WritingAnswers, minimum1: number, minimum2: number): WritingEvaluation {
  const task1 = evaluateTask1(writing.task1, minimum1)
  const task2 = evaluateTask2(writing.task2, minimum2)
  const band = clampBand((task1.band + task2.band * 2) / 3)
  const words1 = countWords(writing.task1)
  const words2 = countWords(writing.task2)
  const feedback: string[] = []
  if (words1 < minimum1) feedback.push(`Task 1 is ${minimum1 - words1} words below the minimum. Under-length answers lose marks for task achievement.`)
  if (words2 < minimum2) feedback.push(`Task 2 is ${minimum2 - words2} words below the minimum. Develop your argument to at least 250 words.`)
  if (words1 >= minimum1 && words2 >= minimum2) feedback.push('Both tasks meet the minimum word count.')
  feedback.push('This is an indicative practice estimate based on the text you produced, not an official IELTS score. A trained examiner also assesses pronunciation and delivery in Speaking.')
  return {
    band,
    criteria: [...task1.criteria, ...task2.criteria],
    feedback,
    task1Words: words1,
    task2Words: words2,
  }
}

export function evaluateSpeaking(attempt: Attempt, totalQuestions: number, words: number): SpeakingEvaluation {
  const answered = attempt.speaking.length
  const totalSeconds = attempt.speaking.reduce((sum, r) => sum + r.seconds, 0)
  const completion = totalQuestions ? Math.min(1, answered / totalQuestions) : 0
  let band = 4 + completion * 2.5
  if (totalSeconds >= 120) band += 0.25
  if (totalSeconds >= 240) band += 0.5
  if (totalSeconds >= 420) band += 0.25
  if (words > 0) {
    const wpm = totalSeconds > 0 ? words / (totalSeconds / 60) : 0
    if (wpm >= 100) band += 0.25
    if (wpm >= 130) band += 0.25
    if (wpm < 60) band -= 0.25
  }
  const notes: string[] = [
    'This is a completion-based practice estimate. It cannot reliably assess pronunciation, fluency or coherence — use the speaking rubric for a fuller self-review.',
  ]
  if (answered < totalQuestions) notes.push(`${totalQuestions - answered} speaking prompt${totalQuestions - answered === 1 ? '' : 's'} were not recorded.`)
  if (totalSeconds > 0) notes.push(`You recorded ${Math.floor(totalSeconds / 60)}m ${totalSeconds % 60}s of speech in total.`)
  if (words > 0) notes.push(`${words} words were transcribed from your recordings.`)
  return { band: clampBand(band), answered, totalQuestions, totalSeconds, words, notes }
}

export function calculateResult(attempt: Attempt, test: TestData, speakingWords: number): AttemptResult {
  const listeningQuestions = test.listening.flatMap((p) => p.questions)
  const readingQuestions = test.reading.flatMap((p) => p.questions)
  const listening = scoreObjective(listeningQuestions, attempt.answers, 'listening')
  const reading = scoreObjective(readingQuestions, attempt.answers, 'reading')
  const writingEvaluation = evaluateWriting(attempt.writing, 150, 250)
  const writing: SectionResult = {
    skill: 'writing',
    band: writingEvaluation.band,
    label: 'Practice estimate',
  }
  const speakingEvaluation = evaluateSpeaking(attempt, test.speaking.reduce((sum, p) => sum + Math.max(1, p.questions.length), 0), speakingWords)
  const speaking: SectionResult = {
    skill: 'speaking',
    band: speakingEvaluation.band,
    label: 'Completion-based estimate',
  }
  const overall = Math.round(((listening.band + reading.band + writing.band + speaking.band) / 4) * 2) / 2
  return {
    attemptId: attempt.id,
    listening,
    reading,
    writing,
    speaking,
    overall,
    completedAt: Date.now(),
    writingEvaluation,
    speakingEvaluation,
  }
}

export function countWritingWords(text: string): number {
  return countWords(text)
}
