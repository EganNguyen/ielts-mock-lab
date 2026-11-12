# Implementation Progress

## Current milestone
M6 — local end-to-end verification

## Completed
- Monorepo: Next.js web app + Go API + PostgreSQL + versioned content.
- PostgreSQL schema: users, sessions, exams, exam versions, attempts, sections, answers, immutable section submissions, speaking recordings, results, audit log.
- Local demo mode with seeded candidate and four seeded Cambridge IELTS 21 Academic tests; production bypass guard.
- Cookie auth with bcrypt + hashed server sessions (used when demo mode is off).
- Server-owned section deadlines, expiry, submission locking, optimistic answer versions, refresh recovery.
- Listening UI: one-play audio, four Kokoro parts, no seeking/pause controls, audio position persistence.
- Reading UI: three passages, split-screen, question palette, flags, TFNG/YNNG, matching headings/information, completion, text-size controls and highlighting.
- Writing UI: Task 1 chart, Task 2 prompt, separate editors, autosave, word counts.
- Speaking UI: three-part examiner flow, Kokoro examiner audio, cue card, preparation timer, MediaRecorder upload, optional browser transcript.
- Results: overall/section bands, answer review with keys and explanations, writing criteria/model answers, speaking recordings/notes, print report.
- Objective scoring tables and local writing/speaking rubrics.
- 4/4/2/3 content structure for all four tests plus writing/map figures.
- Kokoro-82M audio assets for listening and speaking examiner.
- Share showcase link: local Share dialog + `scripts/share.sh`, Cloudflare quick tunnel lifecycle, copy/native share, local-only controls, shutdown cleanup.
- Vocabulary learning pack: 663 sentence-first entries from all 48 Listening parts and 36 Reading passages (IELTS 19 / 20 / Cambridge 21). Every entry has sentence, direct Vietnamese translation, chunk breakdown, why/risk and importance; 242 entries carry 357 verbatim-evidenced answer links, locked until an attempt is confirmed. Interactive `/vocabulary/` page with skill/test/sentence/answer/relationship filters, search and cross-references; validator at `content/vocabulary/tools/verify_learning_vocabulary.py`.
- Go unit tests (including the share manager) and Playwright E2E suite.

## Tests
- Backend: `go test ./...` — pass.
- Frontend build: `pnpm --dir apps/web build` — pass.
- Vocabulary learning pack: `python3 content/vocabulary/tools/verify_learning_vocabulary.py` — pass (663 items, 84 sections, 357 verbatim answer links).
- E2E: `pnpm --dir apps/web exec playwright test --trace=off` — 7/7 pass.
- Browser full-flow: pass (listening → reading → writing → speaking → results → refresh).
- Production demo guard: pass (`APP_ENV=production` + demo mode exits 1).

## Known gaps
- Four-test pack is local/private; confirm publisher rights before redistribution. See `extraction-report.md`.
- No admin content editor UI; content is versioned JSON and reseeded.
- Writing/Speaking estimates are local, not official.
- One original full mock seeded; schema supports more versions.

## Final local verification
- Running: http://127.0.0.1:3000 (demo mode; no login).
- API health: `database:true`, `speechProvider:kokoro-82m-onnx`, `evaluationProvider:local-rubric-v1`.
- Clean database migration/seed verified against a fresh `apex_verify` database.
- Desktop layouts checked at 1440×1000 and 1280×720.
- Demo attempt/test history cleaned after verification.

## Next actions
- Author or license additional exams.
- Add human calibration for Writing/Speaking rubrics if required.
- Add admin publish/validation workflow if content operations expand.
