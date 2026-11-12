# Test Strategy

## Backend
- Answer normalization and accepted alternatives.
- Raw-score band conversion.
- Objective scoring with blanks and wrong answers.
- Writing rubric output shape and word counts.
- Speaking completion metrics.
- Embedded content structure (40/40/2/3).
- Public exam payload must not contain answers, explanations, transcripts or model answers.

Command: `cd services/api && go test ./...`

## Frontend/E2E
Playwright specs assume the local stack is running:
- demo candidate sees the exam without login;
- answer and audio position survive refresh;
- answer keys are absent pre-submission;
- full four-section attempt yields a persisted report;
- Kokoro listening and examiner assets return 200.

Command: `cd apps/web && pnpm exec playwright test`

## Manual acceptance
Verified in Chromium at 1440×1000:
1. Dashboard and exam list load without login.
2. Full mock starts.
3. Listening audio plays and cannot be seeked; answers autosave.
4. Reading split view, question palette and answer review render.
5. Writing tasks accept text and show live word counts.
6. Speaking requests microphone, plays Kokoro prompts, records and uploads audio.
7. Result report generates and survives refresh.
8. Production guard rejects demo mode.
