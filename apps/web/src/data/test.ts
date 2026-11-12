import type { TestData } from '../lib/types'
import { listeningParts } from './listening.ts'
import { readingPassages } from './reading.ts'
import { writingTasks } from './writing.ts'
import { speakingParts } from './speaking.ts'

export const testData: TestData = {
  id: 'apex-academic-01',
  title: 'Academic Mock Test 01',
  module: 'Academic',
  version: '2026.1',
  listening: listeningParts,
  reading: readingPassages,
  writing: writingTasks,
  speaking: speakingParts,
}

export const allListeningQuestions = listeningParts.flatMap((p) => p.questions)
export const allReadingQuestions = readingPassages.flatMap((p) => p.questions)

export const testMeta = {
  listeningMinutes: 30,
  readingMinutes: 60,
  writingMinutes: 60,
  speakingMinutes: 14,
  totalMinutes: 164,
}
