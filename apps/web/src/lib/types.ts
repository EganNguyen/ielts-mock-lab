export type Skill = 'listening' | 'reading' | 'writing' | 'speaking'

export type QuestionType =
  | 'short'
  | 'mcq'
  | 'tfng'
  | 'ynng'
  | 'heading'
  | 'match'
  | 'select'

export interface Question {
  id: string
  number: number
  prompt: string
  type: QuestionType
  answer: string
  accepted?: string[]
  options?: string[]
  explanation: string
  groupId: string
}

export interface QuestionGroup {
  id: string
  label?: string
  instructions: string
  range: [number, number]
  layout?: 'form' | 'notes' | 'table' | 'standard'
  sharedOptions?: string[]
  note?: string
}

export interface ReadingPassage {
  id: string
  number: 1 | 2 | 3
  title: string
  subtitle: string
  paragraphs: { label: string; text: string }[]
  groups: QuestionGroup[]
  questions: Question[]
}

export interface ListeningPart {
  id: string
  number: 1 | 2 | 3 | 4
  title: string
  context: string
  groups: QuestionGroup[]
  questions: Question[]
  transcript: { speaker: string; text: string }[]
}

export interface WritingTask {
  id: string
  number: 1 | 2
  title: string
  prompt: string
  instructions: string[]
  minimumWords: number
  suggestedMinutes: number
  modelAnswer: string
  modelHighlights: string[]
  chart?: 'internet'
}

export interface SpeakingQuestion {
  id: string
  text: string
  followUp?: string
}

export interface SpeakingPart {
  id: string
  number: 1 | 2 | 3
  title: string
  description: string
  questions: SpeakingQuestion[]
  cueCard?: {
    topic: string
    bullets: string[]
    rounding: string
    preparationSeconds: number
    speakingSeconds: number
  }
}

export interface TestData {
  id: string
  title: string
  module: 'Academic'
  version: string
  listening: ListeningPart[]
  reading: ReadingPassage[]
  writing: WritingTask[]
  speaking: SpeakingPart[]
}

export type AnswerMap = Record<string, string>

export interface WritingAnswers {
  task1: string
  task2: string
}

export interface SpeakingResponse {
  questionId: string
  seconds: number
  transcript?: string
}

export interface Attempt {
  id: string
  testId: string
  startedAt: number
  completedAt?: number
  mode: 'full' | Skill
  answers: AnswerMap
  flags: Record<string, boolean>
  writing: WritingAnswers
  speaking: SpeakingResponse[]
  currentSection: Skill
  sectionStartedAt: number
  sectionEndsAt: number
  sectionDurations: Record<Skill, number>
  completedSections: Skill[]
  listeningStarted: boolean
}

export interface SectionResult {
  skill: Skill
  raw?: number
  total?: number
  band: number
  label: string
}

export interface CriterionFeedback {
  name: string
  score: number
  feedback: string
}

export interface WritingEvaluation {
  band: number
  criteria: CriterionFeedback[]
  feedback: string[]
  task1Words: number
  task2Words: number
}

export interface SpeakingEvaluation {
  band: number
  answered: number
  totalQuestions: number
  totalSeconds: number
  words: number
  notes: string[]
}

export interface AttemptResult {
  attemptId: string
  listening: SectionResult
  reading: SectionResult
  writing: SectionResult
  speaking: SectionResult
  overall: number
  completedAt: number
  writingEvaluation: WritingEvaluation
  speakingEvaluation: SpeakingEvaluation
}

export interface SavedAttemptSummary {
  id: string
  startedAt: number
  completedAt: number
  mode: 'full' | Skill
  overall: number
  listening: number
  reading: number
  writing: number
  speaking: number
}
