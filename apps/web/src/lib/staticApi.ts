import type {
  Answer, Attempt, AttemptState, Exam, ExamSummary, Question, Review, Result,
  SectionState, ShareStatus, Skill, User,
} from './api'
import { BASE_PATH } from './assets'
import { calculateResult } from './scoring'
import type { Attempt as LegacyAttempt, TestData } from './types'

const DATA_ROOT = `${BASE_PATH}/data/exams`
const STORE_KEY = 'apex-static-attempts-v1'
const ORDER: Skill[] = ['listening', 'reading', 'writing', 'speaking']
const DURATIONS: Record<Skill, number> = {
  listening: 1800, reading: 3600, writing: 3600, speaking: 900,
}

type LocalAnswer = { questionId: string; value: string; version: number }
type LocalSpeaking = { questionId: string; part: number; durationSeconds: number; transcript?: string }
type LocalAttempt = {
  id: string
  examId: string
  mode: string
  status: string
  currentSkill: Skill
  startedAt: string
  completedAt?: string
  sections: SectionState[]
  answers: Record<string, LocalAnswer>
  speaking: LocalSpeaking[]
  result?: Result
}

type Store = Record<string, LocalAttempt>

let indexCache: ExamSummary[] | null = null
const examCache = new Map<string, Exam>()

function fail(status: number, code: string, message: string): never {
  const error = new Error(message) as Error & { status: number; code: string }
  error.status = status
  error.code = code
  throw error
}

function now() { return new Date() }
function iso(date: Date) { return date.toISOString() }

function readStore(): Store {
  if (typeof window === 'undefined') return {}
  try {
    const raw = window.localStorage.getItem(STORE_KEY)
    const parsed = raw ? JSON.parse(raw) : {}
    return parsed && typeof parsed === 'object' ? parsed as Store : {}
  } catch {
    return {}
  }
}

function writeStore(store: Store) {
  if (typeof window === 'undefined') return
  try {
    window.localStorage.setItem(STORE_KEY, JSON.stringify(store))
  } catch {
    // A full or unavailable storage must not interrupt an exam.
  }
}

async function getIndex(): Promise<ExamSummary[]> {
  if (indexCache) return indexCache
  const response = await fetch(`${DATA_ROOT}/index.json`)
  if (!response.ok) fail(response.status, 'DATA_MISSING', 'Static exam data is missing')
  const data = await response.json() as { exams: ExamSummary[] }
  indexCache = data.exams
  return data.exams
}

async function getExam(id: string): Promise<Exam> {
  const cached = examCache.get(id)
  if (cached) return cached
  const response = await fetch(`${DATA_ROOT}/${id}.json`)
  if (!response.ok) fail(404, 'EXAM_NOT_FOUND', 'Exam not found')
  const exam = await response.json() as Exam
  examCache.set(id, exam)
  return exam
}

function durationFor(skill: Skill) { return DURATIONS[skill] ?? 1800 }
function nextSkill(skill: Skill): Skill | undefined { return ORDER[ORDER.indexOf(skill) + 1] }

function refresh(local: LocalAttempt) {
  const time = now()
  for (const section of local.sections) {
    if (section.status === 'in_progress' && section.deadlineAt && Date.parse(section.deadlineAt) <= time.getTime()) {
      section.status = 'expired'
      section.submittedAt = section.deadlineAt
    }
    if (section.deadlineAt && (section.status === 'in_progress' || section.status === 'expired')) {
      section.remainingSeconds = Math.max(0, Math.floor((Date.parse(section.deadlineAt) - time.getTime()) / 1000))
    } else if (section.status === 'not_started') {
      section.remainingSeconds = section.durationSeconds
    } else {
      section.remainingSeconds = 0
    }
  }
}

function writingFrom(local: LocalAttempt) {
  return {
    task1: local.answers['writing-task-1']?.value ?? '',
    task2: local.answers['writing-task-2']?.value ?? '',
  }
}

function stateFor(local: LocalAttempt, exam: Exam): AttemptState {
  refresh(local)
  const answers: Record<string, Answer> = {}
  Object.values(local.answers).forEach((answer) => { answers[answer.questionId] = answer })
  return {
    attempt: {
      id: local.id,
      examId: local.examId,
      mode: local.mode,
      status: local.status,
      currentSkill: local.currentSkill,
      startedAt: local.startedAt,
      completedAt: local.completedAt,
      sections: local.sections,
    },
    exam,
    answers,
    writing: writingFrom(local),
    speaking: local.speaking.map((response) => ({
      questionId: response.questionId,
      durationSeconds: response.durationSeconds,
      transcript: response.transcript,
      part: response.part,
    })),
    serverTime: iso(now()),
  }
}

function load(id: string) {
  const local = readStore()[id]
  if (!local) fail(404, 'ATTEMPT_NOT_FOUND', 'Attempt not found')
  return local
}

function save(local: LocalAttempt) {
  const store = readStore()
  store[local.id] = local
  writeStore(store)
}

function countWords(text: string) {
  return text.trim() ? text.trim().split(/\s+/).filter((word) => /[A-Za-z0-9’'-]/.test(word)).length : 0
}

function buildResult(local: LocalAttempt, exam: Exam): Result {
  const answers: Record<string, string> = {}
  Object.values(local.answers).forEach((answer) => { answers[answer.questionId] = answer.value })
  const writing = writingFrom(local)
  const speakingWords = local.speaking.reduce((sum, response) => sum + countWords(response.transcript ?? ''), 0)
  const legacy: LegacyAttempt = {
    id: local.id,
    testId: local.examId,
    startedAt: Date.parse(local.startedAt),
    completedAt: Date.now(),
    mode: local.mode as LegacyAttempt['mode'],
    answers,
    flags: {},
    writing,
    speaking: local.speaking.map((response) => ({
      questionId: response.questionId,
      seconds: response.durationSeconds,
      transcript: response.transcript,
    })),
    currentSection: local.currentSkill,
    sectionStartedAt: 0,
    sectionEndsAt: 0,
    sectionDurations: DURATIONS,
    completedSections: local.sections.filter((section) => section.status === 'submitted').map((section) => section.skill),
    listeningStarted: true,
  }
  const calculated = calculateResult(legacy, exam as unknown as TestData, speakingWords)
  return {
    attemptId: local.id,
    examTitle: exam.title,
    mode: local.mode,
    listening: { ...calculated.listening, raw: calculated.listening.raw ?? 0, total: calculated.listening.total ?? 40 },
    reading: { ...calculated.reading, raw: calculated.reading.raw ?? 0, total: calculated.reading.total ?? 40 },
    writing: calculated.writing,
    speaking: calculated.speaking,
    overall: calculated.overall,
    completedAt: iso(new Date(calculated.completedAt)),
    writingEvaluation: calculated.writingEvaluation,
    speakingEvaluation: calculated.speakingEvaluation,
    official: false,
  }
}

const demoUser: User = {
  id: 'static-demo-candidate',
  email: 'demo@apex.local',
  displayName: 'Demo Candidate',
  role: 'candidate',
}

const inactiveShare: ShareStatus = {
  active: false,
  starting: false,
  provider: 'static',
  target: '',
  available: false,
  message: 'Sharing is not available in the static build.',
}

export const staticApi = {
  me: async () => ({ user: demoUser, demoMode: true }),

  config: async () => ({ demoMode: true, evaluationProvider: 'local-rubric-v1', speechProvider: 'local-files' }),

  exams: async () => ({ exams: await getIndex() }),

  exam: async (id: string) => getExam(id),

  createAttempt: async (examId: string, mode: 'full' | Skill) => {
    const exam = await getExam(examId)
    const skills = mode === 'full' ? ORDER : [mode]
    const id = `local-${crypto.randomUUID()}`
    const startedAt = iso(now())
    const local: LocalAttempt = {
      id,
      examId,
      mode,
      status: 'in_progress',
      currentSkill: skills[0],
      startedAt,
      sections: skills.map((skill) => ({
        skill,
        status: 'not_started',
        durationSeconds: durationFor(skill),
        remainingSeconds: durationFor(skill),
      })),
      answers: {},
      speaking: [],
    }
    save(local)
    return stateFor(local, exam)
  },

  attempt: async (id: string) => {
    const local = load(id)
    const exam = await getExam(local.examId)
    refresh(local)
    save(local)
    return stateFor(local, exam)
  },

  startSection: async (id: string, skill: Skill) => {
    const local = load(id)
    if (local.status === 'completed') fail(409, 'ATTEMPT_CLOSED', 'This attempt is complete')
    if (local.mode !== 'full' && local.mode !== skill) fail(403, 'FORBIDDEN', 'This skill is not part of the attempt')
    const section = local.sections.find((item) => item.skill === skill)
    if (!section) fail(404, 'SECTION_NOT_FOUND', 'Section not found')
    if (section.status === 'submitted' || section.status === 'expired') {
      fail(409, 'SECTION_CLOSED', 'This section is already closed')
    }
    if (section.status === 'not_started' && local.mode === 'full') {
      const index = ORDER.indexOf(skill)
      if (index > 0) {
        const previous = local.sections.find((item) => item.skill === ORDER[index - 1])
        if (!previous || (previous.status !== 'submitted' && previous.status !== 'expired')) {
          fail(409, 'PREVIOUS_SECTION', 'The previous section is not complete')
        }
      }
    }
    if (section.status === 'not_started') {
      const start = now()
      section.status = 'in_progress'
      section.startedAt = iso(start)
      section.deadlineAt = iso(new Date(start.getTime() + section.durationSeconds * 1000))
    }
    local.currentSkill = skill
    local.status = 'in_progress'
    save(local)
    return stateFor(local, await getExam(local.examId))
  },

  saveAnswer: async (id: string, skill: Skill, questionId: string, value: string, version: number) => {
    const local = load(id)
    const section = local.sections.find((item) => item.skill === skill)
    if (!section) fail(404, 'SECTION_NOT_FOUND', 'Section not found')
    refresh(local)
    if (section.status !== 'in_progress') fail(409, 'SECTION_CLOSED', 'This section is closed')
    const previous = local.answers[questionId]
    const nextVersion = (previous?.version ?? 0) + 1
    local.answers[questionId] = { questionId, value, version: nextVersion }
    save(local)
    return { questionId, value, version: nextVersion }
  },

  submitSection: async (id: string, skill: Skill) => {
    const local = load(id)
    const section = local.sections.find((item) => item.skill === skill)
    if (!section) fail(404, 'SECTION_NOT_FOUND', 'Section not found')
    refresh(local)
    if (section.status === 'in_progress' || section.status === 'expired' || section.status === 'not_started') {
      section.status = 'submitted'
      section.submittedAt = iso(now())
    }
    if (local.mode === 'full') {
      const next = nextSkill(skill)
      if (next) local.currentSkill = next
      else local.status = 'core_submitted'
    } else {
      local.status = 'core_submitted'
    }
    save(local)
    return stateFor(local, await getExam(local.examId))
  },

  speaking: async (id: string, form: FormData) => {
    const local = load(id)
    const questionId = String(form.get('questionId') ?? '')
    const part = Number(form.get('part') ?? 1)
    const durationSeconds = Math.max(1, Number(form.get('durationSeconds') ?? 1))
    const transcript = String(form.get('transcript') ?? '')
    const existing = local.speaking.find((item) => item.questionId === questionId)
    if (existing) {
      existing.part = part
      existing.durationSeconds = durationSeconds
      existing.transcript = transcript
    } else {
      local.speaking.push({ questionId, part, durationSeconds, transcript })
    }
    save(local)
    return { questionId, durationSeconds, audioUrl: '' }
  },

  complete: async (id: string) => {
    const local = load(id)
    if (local.result) return local.result
    const exam = await getExam(local.examId)
    refresh(local)
    for (const section of local.sections) {
      if (section.status === 'not_started' || section.status === 'in_progress' || section.status === 'expired') {
        section.status = 'submitted'
        section.submittedAt = section.submittedAt ?? iso(now())
      }
    }
    local.status = 'completed'
    local.completedAt = iso(now())
    const result = buildResult(local, exam)
    local.result = result
    save(local)
    return result
  },

  result: async (id: string) => {
    const local = load(id)
    if (!local.result) fail(404, 'RESULT_NOT_FOUND', 'Result not available')
    return local.result
  },

  review: async (id: string): Promise<Review> => {
    const local = load(id)
    if (!local.result) fail(403, 'RESULT_NOT_READY', 'Complete the test to view the result')
    const exam = await getExam(local.examId)
    const state = stateFor(local, exam)
    return {
      attempt: state.attempt,
      exam,
      answers: state.answers,
      writing: state.writing,
      speaking: state.speaking,
      result: local.result,
    }
  },

  history: async () => {
    const completed = Object.values(readStore())
      .filter((local) => local.result)
      .sort((a, b) => Date.parse(b.result!.completedAt) - Date.parse(a.result!.completedAt))
      .slice(0, 20)
      .map((local) => ({
        id: local.id,
        mode: local.mode,
        startedAt: local.startedAt,
        completedAt: local.result!.completedAt,
        overall: local.result!.overall,
        listening: local.result!.listening.band,
        reading: local.result!.reading.band,
        writing: local.result!.writing.band,
        speaking: local.result!.speaking.band,
      }))
    return { attempts: completed }
  },

  activeAttempt: async () => {
    const active = Object.values(readStore())
      .filter((local) => local.status !== 'completed')
      .sort((a, b) => Date.parse(b.startedAt) - Date.parse(a.startedAt))[0]
    if (!active) return { attempt: null }
    const exams = await getIndex()
    const summary = exams.find((exam) => exam.id === active.examId)
    return {
      attempt: {
        id: active.id,
        mode: active.mode,
        currentSkill: active.currentSkill,
        title: summary?.title ?? active.examId,
        status: active.status,
        startedAt: active.startedAt,
      },
    }
  },

  share: async () => inactiveShare,
  startShare: async () => inactiveShare,
  stopShare: async () => inactiveShare,
}
