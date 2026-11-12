# Implementation Status

## Fully implemented
- One seeded original Academic mock across four skills.
- Exam lifecycle, server deadlines, autosave, answer versions, section locking, refresh recovery.
- Listening/reading/writing/speaking candidate UIs.
- Kokoro-82M voice assets for listening and speaking.
- Deterministic objective scoring.
- Local writing/speaking estimate provider with explicit non-official labelling.
- Results, answer review, model answers, recordings playback, print report.
- One-click share link for the local showcase via a Cloudflare quick tunnel, with copy/native-share/stop controls and local-only tunnel management.
- Local demo mode, cookie auth, production demo guard.
- PostgreSQL migrations/seed on API startup.
- Go unit tests and Playwright E2E tests.

## Implemented with local mocks
- Writing evaluation: deterministic local rubric.
- Speaking evaluation: completion/duration/transcript heuristic.
- Speech transcription: browser API when available; no paid provider required.

## Requires external configuration
- None for local use.
- Additional exams require licensed content or original authoring.
- Official scoring would require trained examiners or a calibrated provider.

## Not implemented
- Import of Cambridge IELTS 21 (copyright restriction).
- Admin content editor UI.
- Multiple authored full mock tests.
