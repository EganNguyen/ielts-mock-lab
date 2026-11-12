#!/usr/bin/env node
/**
 * Copy the seeded exam packs into the web app's public folder for static export.
 * The static build has no API: the browser loads these JSON files and scores locally.
 */
import { mkdir, readFile, writeFile } from 'node:fs/promises'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = join(dirname(fileURLToPath(import.meta.url)), '..')
const source = join(root, 'content', 'academic')
const target = join(root, 'apps', 'web', 'public', 'data', 'exams')
const packs = ['cambridge21', 'ielts20', 'ielts19']
const summaries = []

await mkdir(target, { recursive: true })

for (const pack of packs) {
  for (let test = 1; test <= 4; test += 1) {
    const id = `${pack}-test${test}`
    const raw = await readFile(join(source, `${id}.json`), 'utf8')
    const exam = JSON.parse(raw)
    await writeFile(join(target, `${id}.json`), raw)
    summaries.push({
      id: exam.id,
      code: exam.id,
      title: exam.title,
      module: exam.module,
      version: exam.version,
      durationMinutes: 164,
      listeningQuestions: exam.listening.reduce((sum, part) => sum + part.questions.length, 0),
      readingQuestions: exam.reading.reduce((sum, part) => sum + part.questions.length, 0),
      writingTasks: exam.writing.length,
      speakingParts: exam.speaking.length,
    })
  }
}

summaries.sort((a, b) => {
  const year = (item) => Number(item.title.match(/IELTS\s+(\d+)/)?.[1] ?? 0)
  return year(b) - year(a) || a.id.localeCompare(b.id)
})
await writeFile(join(target, 'index.json'), JSON.stringify({ exams: summaries }, null, 2) + '\n')
console.log(`prepared ${summaries.length} static exams in ${target}`)
