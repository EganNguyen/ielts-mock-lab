import { expect, test } from '@playwright/test'

test('dashboard exposes both Cambridge 21 and IELTS 20 packs', async ({ page }) => {
  await page.goto('/')
  await expect(page.getByRole('heading', { name: /The full test/i })).toBeVisible()
  await expect(page.locator('.test-chip')).toHaveCount(8)
  await expect(page.locator('.mock-card h3')).toContainText('Cambridge IELTS 21')
  await expect(page.getByText('Demo Candidate', { exact: false }).first()).toBeVisible()
  await expect(page.getByRole('button', { name: /Start full mock test/i })).toBeEnabled()
  await page.locator('.test-chip').nth(3).click()
  await expect(page.locator('.mock-card h3')).toContainText('Cambridge IELTS 21 · Academic Test 4')
  await page.locator('.test-chip').nth(4).click()
  await expect(page.locator('.mock-card h3')).toContainText('IELTS 20 · Academic Test 1')
  await page.locator('.test-chip').nth(7).click()
  await expect(page.locator('.mock-card h3')).toContainText('IELTS 20 · Academic Test 4')
})

test('an IELTS 20 test opens with its own paper and audio', async ({ page }) => {
  await page.goto('/')
  await page.locator('.test-chip').nth(4).click()
  await expect(page.locator('.mock-card h3')).toContainText('IELTS 20 · Academic Test 1')
  await page.getByRole('button', { name: /Begin full test/i }).click()
  await page.waitForURL(/\/exam\//)
  await expect(page.locator('.part-banner')).toContainText('Part 1')
  await expect(page.getByRole('heading', { name: 'Choosing a restaurant' })).toBeVisible()
  await expect(page.getByLabel('Answer for question 1', { exact: true })).toBeVisible()
  await expect(page.getByLabel('Answer for question 10', { exact: true })).toBeVisible()
})

test('answers and the one-play audio survive a refresh', async ({ page }) => {
  await page.goto('/')
  await page.getByRole('button', { name: /Start full mock test/i }).click()
  await page.waitForURL(/\/exam\//)
  await expect(page.locator('.exam-timer')).toBeVisible()
  await expect(page.locator('.part-banner')).toContainText('Part 1')
  const play = page.getByRole('button', { name: /Play recording|Resume recording|Play exam audio/i })
  if (await play.count()) await play.click()

  const attemptUrl = page.url()
  await page.getByLabel('Answer for question 1', { exact: true }).fill('10')
  await page.getByLabel('Answer for question 2', { exact: true }).fill('weather')
  await expect(page.locator('.exam-autosave')).toContainText('Saved', { timeout: 10_000 })
  await page.waitForTimeout(1300)
  await page.reload({ waitUntil: 'networkidle' })
  expect(page.url()).toBe(attemptUrl)
  await expect(page.getByLabel('Answer for question 1', { exact: true })).toHaveValue('10')
  await expect(page.getByLabel('Answer for question 2', { exact: true })).toHaveValue('weather')
  await expect(page.locator('.exam-timer')).toBeVisible()
  await expect(page.getByRole('button', { name: /Play recording|Resume recording|Play exam audio/i })).toBeVisible()
})

test('a completed Cambridge 21 attempt scores against the book answer key', async ({ request }) => {
  const create = await request.post('/api/v1/exams/cambridge21-test1/attempts', { data: { mode: 'full' } })
  expect(create.status()).toBe(201)
  const state = await create.json()
  const id = state.attempt.id

  const answers: Record<string, string> = {
    'l1-q1': '10', 'l1-q2': 'weather', 'l1-q3': 'safety', 'l1-q4': 'discount', 'l1-q5': 'dictionary',
    'l1-q6': 'certificate', 'l1-q7': 'towel', 'l1-q8': 'cafe', 'l1-q9': 'videos', 'l1-q10': 'Lockers',
    'l2-q11': 'A', 'l2-q12': 'B', 'l2-q13': 'A', 'l2-q14': 'A', 'l2-q15': 'A', 'l2-q16': 'C',
    'l2-q17': 'C', 'l2-q18': 'A', 'l2-q19': 'B', 'l2-q20': 'C',
    'l3-q21': 'B', 'l3-q22': 'D', 'l3-q23': 'C', 'l3-q24': 'E', 'l3-q25': 'G', 'l3-q26': 'B',
    'l3-q27': 'F', 'l3-q28': 'H', 'l3-q29': 'A', 'l3-q30': 'E',
    'l4-q31': 'metal', 'l4-q32': 'slow', 'l4-q33': 'demand', 'l4-q34': 'equator', 'l4-q35': 'recycle',
    'l4-q36': 'fungus', 'l4-q37': 'weather', 'l4-q38': 'strong', 'l4-q39': 'roots', 'l4-q40': 'soil',
    'r1-q1': 'mining', 'r1-q2': 'education', 'r1-q3': 'notes', 'r1-q4': 'journals', 'r1-q5': 'Venice',
    'r1-q6': 'canteen', 'r1-q7': 'friends', 'r1-q8': 'TRUE', 'r1-q9': 'NOT GIVEN', 'r1-q10': 'FALSE',
    'r1-q11': 'NOT GIVEN', 'r1-q12': 'TRUE', 'r1-q13': 'TRUE',
    'r2-q14': 'C', 'r2-q15': 'B', 'r2-q16': 'A', 'r2-q17': 'G', 'r2-q18': 'breath',
    'r2-q19': 'questionnaire', 'r2-q20': 'wellbeing', 'r2-q21': 'depression',
    'r2-q22': 'C', 'r2-q23': 'A', 'r2-q24': 'B', 'r2-q25': 'D', 'r2-q26': 'C',
    'r3-q27': 'B', 'r3-q28': 'A', 'r3-q29': 'C', 'r3-q30': 'A', 'r3-q31': 'H', 'r3-q32': 'E',
    'r3-q33': 'I', 'r3-q34': 'A', 'r3-q35': 'G', 'r3-q36': 'C', 'r3-q37': 'YES',
    'r3-q38': 'NOT GIVEN', 'r3-q39': 'NO', 'r3-q40': 'YES',
  }
  await request.post(`/api/v1/attempts/${id}/sections/listening/start`)
  for (const [questionId, value] of Object.entries(answers).filter(([key]) => key.startsWith('l'))) {
    const save = await request.put(`/api/v1/attempts/${id}/sections/listening/answers/${questionId}`, { data: { value, version: 0 } })
    expect(save.ok()).toBeTruthy()
  }
  await request.post(`/api/v1/attempts/${id}/sections/listening/submit`)
  await request.post(`/api/v1/attempts/${id}/sections/reading/start`)
  for (const [questionId, value] of Object.entries(answers).filter(([key]) => key.startsWith('r'))) {
    await request.put(`/api/v1/attempts/${id}/sections/reading/answers/${questionId}`, { data: { value, version: 0 } })
  }
  await request.post(`/api/v1/attempts/${id}/sections/reading/submit`)
  await request.post(`/api/v1/attempts/${id}/sections/writing/start`)
  await request.put(`/api/v1/attempts/${id}/sections/writing/answers/writing-task-1`, { data: { value: 'The graph shows change over time. '.repeat(20), version: 0 } })
  await request.put(`/api/v1/attempts/${id}/sections/writing/answers/writing-task-2`, { data: { value: 'Housing is an important public issue. '.repeat(30), version: 0 } })
  await request.post(`/api/v1/attempts/${id}/sections/writing/submit`)
  await request.post(`/api/v1/attempts/${id}/sections/speaking/start`)
  await request.post(`/api/v1/attempts/${id}/sections/speaking/submit`)
  const complete = await request.post(`/api/v1/attempts/${id}/complete`)
  expect(complete.ok()).toBeTruthy()
  const result = await complete.json()
  expect(result.listening.raw).toBe(40)
  expect(result.reading.raw).toBe(40)
  expect(result.examTitle).toContain('Test 1')

  const page = await request.get(`/api/v1/attempts/${id}/review`)
  const review = await page.json()
  expect(review.exam.listening[0].questions[0].answer).toBe('10')
})

test('answer keys are not exposed before submission', async ({ request }) => {
  const response = await request.get('/api/v1/exams/cambridge21-test1')
  expect(response.ok()).toBeTruthy()
  const exam = await response.json()
  expect(exam.listening[0].questions[0].answer).toBeUndefined()
  expect(exam.listening[0].questions[0].explanation).toBeUndefined()
  expect(exam.listening[0].transcript).toBeUndefined()
  expect(exam.writing[0].modelAnswer).toBeUndefined()
  expect(exam.audioUrl).toBe('/media/listening/cambridge21-test1')
})

test('Kokoro listening, figures and examiner audio are served locally', async ({ request }) => {
  const assets = [
    '/media/listening/cambridge21-test1/part1.mp3',
    '/media/figures/cambridge21/test1-writing-task1.jpg',
    '/media/figures/cambridge21/test2-listening-map.jpg',
    '/media/speaking/examiner/cambridge21-test1/intro.mp3',
    '/media/speaking/examiner/cambridge21-test1/s1.mp3',
  ]
  for (const path of assets) {
    const response = await request.get(path)
    expect(response.ok(), `${path} should be available`).toBeTruthy()
    expect(Number(response.headers()['content-length'] || 0)).toBeGreaterThan(1000)
  }
})

test('share status reports the quick-tunnel provider', async ({ request }) => {
  const response = await request.get('/api/v1/share')
  expect(response.ok()).toBeTruthy()
  const status = await response.json()
  expect(status.provider).toBe('cloudflare-quick-tunnel')
  expect(typeof status.active).toBe('boolean')
  expect(typeof status.available).toBe('boolean')
})

test('dashboard opens the share showcase dialog', async ({ page }) => {
  await page.goto('/')
  await page.getByRole('button', { name: /Share this showcase/i }).click()
  const dialog = page.getByRole('dialog', { name: 'Share this showcase' })
  await expect(dialog).toBeVisible()
  await expect(dialog.getByText(/Private showcase, shared demo candidate/i)).toBeVisible()
})
