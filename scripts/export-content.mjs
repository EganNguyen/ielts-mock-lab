import fs from 'node:fs'
import path from 'node:path'
import { testData } from '../apps/web/src/data/test.ts'

const out = {
  ...testData,
  publishedAt: new Date().toISOString(),
  scoring: {
    listeningVersion: 'ielts-academic-public-2024',
    readingVersion: 'ielts-academic-public-2024',
    rubricVersion: 'apex-local-rubric-v1',
  },
}

const dir = path.join(process.cwd(), 'content', 'academic')
fs.mkdirSync(dir, { recursive: true })
const json = JSON.stringify(out, null, 2)
fs.writeFileSync(path.join(dir, 'test001.json'), json)
fs.writeFileSync(path.join(process.cwd(), 'services/api/internal/content/test001.json'), json)
const listening = testData.listening.reduce((n, p) => n + p.questions.length, 0)
const reading = testData.reading.reduce((n, p) => n + p.questions.length, 0)
console.log(`Wrote content/academic/test001.json — listening ${listening}, reading ${reading}, writing ${testData.writing.length}, speaking ${testData.speaking.length}`)
