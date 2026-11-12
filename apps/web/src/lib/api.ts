export type Skill = 'listening' | 'reading' | 'writing' | 'speaking'

export interface Question {
  id: string
  number: number
  groupId: string
  type: 'short' | 'mcq' | 'tfng' | 'ynng' | 'heading' | 'match' | 'select' | 'map'
  prompt: string
  options?: string[]
  accepted?: string[]
  explanation?: string
  answer?: string
}

export interface QuestionGroup {
  id: string
  label?: string
  instructions: string
  range: [number, number]
  layout?: 'form' | 'notes' | 'table' | 'standard' | 'summary' | 'flow' | 'match' | 'map'
  sharedOptions?: string[]
  note?: string
  body?: string[]
  figure?: string
  figureAlt?: string
}

export interface ListeningPart {
  id: string
  number: number
  title: string
  context: string
  groups: QuestionGroup[]
  questions: Question[]
  transcript?: { speaker: string; text: string }[]
}

export interface ReadingPassage {
  id: string
  number: number
  title: string
  subtitle: string
  paragraphs: { label: string; text: string }[]
  groups: QuestionGroup[]
  questions: Question[]
}

export interface WritingTask {
  id: string
  number: number
  title: string
  prompt: string
  instructions: string[]
  minimumWords: number
  suggestedMinutes: number
  modelAnswer?: string
  modelHighlights?: string[]
  chart?: 'internet'
  figure?: string
  figureAlt?: string
}

export interface SpeakingQuestion {
  id: string
  text: string
  followUp?: string
}

export interface CueCard {
  topic: string
  bullets: string[]
  rounding: string
  preparationSeconds: number
  speakingSeconds: number
}

export interface SpeakingPart {
  id: string
  number: number
  title: string
  description: string
  questions: SpeakingQuestion[]
  cueCard?: CueCard
}

export interface Exam {
  id: string
  title: string
  module: string
  version: string
  listening: ListeningPart[]
  reading: ReadingPassage[]
  writing: WritingTask[]
  speaking: SpeakingPart[]
  audioUrl?: string
  scoring?: { listeningVersion: string; readingVersion: string; rubricVersion: string }
}

export interface ExamSummary {
  id: string
  code: string
  title: string
  module: string
  version: string
  durationMinutes: number
  listeningQuestions: number
  readingQuestions: number
  writingTasks: number
  speakingParts: number
}

export interface SectionState {
  skill: Skill
  status: 'not_started' | 'in_progress' | 'submitted' | 'expired'
  startedAt?: string
  deadlineAt?: string
  submittedAt?: string
  durationSeconds: number
  remainingSeconds: number
}

export interface Attempt {
  id: string
  examId: string
  mode: string
  status: string
  currentSkill: Skill
  startedAt: string
  completedAt?: string
  sections: SectionState[]
}

export interface Answer {
  questionId: string
  value: string
  version: number
}

export interface AttemptState {
  attempt: Attempt
  exam: Exam
  answers: Record<string, Answer>
  writing: { task1: string; task2: string }
  speaking: Array<{ questionId: string; durationSeconds: number; transcript?: string; audioUrl?: string; part: number }>
  serverTime: string
}

export interface Criterion {
  name: string
  score: number
  feedback: string
}

export interface Result {
  attemptId: string
  examTitle?: string
  mode: string
  listening: { skill: string; raw: number; total: number; band: number; label: string }
  reading: { skill: string; raw: number; total: number; band: number; label: string }
  writing: { skill: string; band: number; label: string }
  speaking: { skill: string; band: number; label: string }
  overall: number
  completedAt: string
  writingEvaluation: {
    band: number
    criteria: Criterion[]
    feedback: string[]
    task1Words: number
    task2Words: number
  }
  speakingEvaluation: {
    band: number
    answered: number
    totalQuestions: number
    totalSeconds: number
    words: number
    notes: string[]
  }
  official: boolean
}

export interface Review {
  attempt: Attempt
  exam: Exam
  answers: Record<string, Answer>
  writing: { task1: string; task2: string }
  speaking: Array<{ questionId: string; durationSeconds: number; transcript?: string; audioUrl?: string; part: number }>
  result: Result
}

export interface User {
  id: string
  email: string
  displayName: string
  role: string
}

export interface ShareStatus {
  active: boolean
  starting: boolean
  url?: string
  provider: string
  target: string
  available: boolean
  startedAt?: string
  message?: string
}

export class ApiError extends Error {
  status: number
  code: string
  constructor(status: number, code: string, message: string) {
    super(message)
    this.status = status
    this.code = code
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`/api/v1${path}`, {
    credentials: 'include',
    ...init,
    headers: {
      ...(init?.body instanceof FormData ? {} : { 'Content-Type': 'application/json' }),
      ...init?.headers,
    },
  })
  if (!response.ok) {
    const payload = await response.json().catch(() => null)
    throw new ApiError(
      response.status,
      payload?.error?.code ?? 'REQUEST_FAILED',
      payload?.error?.message ?? `Request failed (${response.status})`,
    )
  }
  return response.json() as Promise<T>
}

export const api = {
  me: () => request<{ user: User; demoMode: boolean }>('/auth/me'),
  config: () => request<{ demoMode: boolean; evaluationProvider: string; speechProvider: string }>('/config'),
  exams: () => request<{ exams: ExamSummary[] }>('/exams'),
  exam: (id: string) => request<Exam>(`/exams/${id}`),
  createAttempt: (examId: string, mode: 'full' | Skill) =>
    request<AttemptState>(`/exams/${examId}/attempts`, { method: 'POST', body: JSON.stringify({ mode }) }),
  attempt: (id: string) => request<AttemptState>(`/attempts/${id}`),
  startSection: (id: string, skill: Skill) =>
    request<AttemptState>(`/attempts/${id}/sections/${skill}/start`, { method: 'POST' }),
  saveAnswer: (id: string, skill: Skill, questionId: string, value: string, version: number) =>
    request<Answer>(`/attempts/${id}/sections/${skill}/answers/${encodeURIComponent(questionId)}`, {
      method: 'PUT',
      body: JSON.stringify({ value, version }),
    }),
  submitSection: (id: string, skill: Skill) =>
    request<AttemptState>(`/attempts/${id}/sections/${skill}/submit`, { method: 'POST' }),
  speaking: (id: string, form: FormData) =>
    request<{ questionId: string; durationSeconds: number; audioUrl: string }>(`/attempts/${id}/speaking`, {
      method: 'POST',
      body: form,
    }),
  complete: (id: string) => request<Result>(`/attempts/${id}/complete`, { method: 'POST' }),
  result: (id: string) => request<Result>(`/attempts/${id}/results`),
  review: (id: string) => request<Review>(`/attempts/${id}/review`),
  history: () =>
    request<{ attempts: Array<{ id: string; mode: string; startedAt: string; completedAt: string; overall: number; listening: number; reading: number; writing: number; speaking: number }> }>('/history'),
  activeAttempt: () =>
    request<{ attempt: { id: string; mode: string; currentSkill: string; title: string; status: string; startedAt: string } | null }>('/attempts/active'),
  share: () => request<ShareStatus>('/share'),
  startShare: () => request<ShareStatus>('/share', { method: 'POST' }),
  stopShare: () => request<ShareStatus>('/share', { method: 'DELETE' }),
}
