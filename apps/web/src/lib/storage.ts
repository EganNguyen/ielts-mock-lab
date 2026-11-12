import type { Attempt, AttemptResult, SavedAttemptSummary } from './types'

const DRAFT_KEY = 'apex-ielts-draft-v1'
const HISTORY_KEY = 'apex-ielts-history-v1'
const LAST_RESULT_KEY = 'apex-ielts-last-result-v1'

export function saveDraft(attempt: Attempt | null) {
  try {
    if (!attempt) localStorage.removeItem(DRAFT_KEY)
    else localStorage.setItem(DRAFT_KEY, JSON.stringify(attempt))
  } catch {
    // A full or unavailable storage should never interrupt an exam.
  }
}

export function loadDraft(): Attempt | null {
  try {
    const raw = localStorage.getItem(DRAFT_KEY)
    if (!raw) return null
    const parsed = JSON.parse(raw) as Attempt
    if (!parsed?.id || !parsed?.testId) return null
    return parsed
  } catch {
    return null
  }
}

export function clearDraft() {
  try {
    localStorage.removeItem(DRAFT_KEY)
  } catch {
    // ignore
  }
}

export function loadHistory(): SavedAttemptSummary[] {
  try {
    const raw = localStorage.getItem(HISTORY_KEY)
    if (!raw) return []
    const parsed = JSON.parse(raw)
    return Array.isArray(parsed) ? parsed : []
  } catch {
    return []
  }
}

export function addHistory(summary: SavedAttemptSummary): SavedAttemptSummary[] {
  const history = loadHistory()
  const next = [summary, ...history.filter((item) => item.id !== summary.id)].slice(0, 20)
  try {
    localStorage.setItem(HISTORY_KEY, JSON.stringify(next))
  } catch {
    // ignore
  }
  return next
}


export interface StoredResult {
  attempt: Attempt
  result: AttemptResult
}

export function saveLastResult(value: StoredResult | null) {
  try {
    if (!value) localStorage.removeItem(LAST_RESULT_KEY)
    else localStorage.setItem(LAST_RESULT_KEY, JSON.stringify(value))
  } catch {
    // ignore
  }
}

export function loadLastResult(): StoredResult | null {
  try {
    const raw = localStorage.getItem(LAST_RESULT_KEY)
    if (!raw) return null
    const parsed = JSON.parse(raw) as StoredResult
    if (!parsed?.attempt || !parsed?.result) return null
    return parsed
  } catch {
    return null
  }
}
