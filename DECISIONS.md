# Decisions

## D001 — One local-first monorepo
Next.js candidate app, Go API, PostgreSQL, content JSON. This keeps the exam engine deterministic and avoids a second content schema.

## D002 — Server-owned time
Section deadlines live in `attempt_sections.deadline_at`. The client renders the countdown, but save/submit endpoints reject writes after the deadline or after submission.

## D003 — Answer keys never in candidate payloads
`model.Exam.Public()` zeroes answers, accepted alternatives, explanations, listening transcripts and writing model answers. Review is a separate completed-only endpoint.

## D004 — Immutable section snapshots
On submit, a JSON snapshot and checksum is written to `section_submissions` with `ON CONFLICT DO NOTHING`. Answers are rejected once the section is submitted.

## D005 — Local evaluation provider
Writing and Speaking are scored with a deterministic local rubric provider. Output is explicitly labelled `official: false`. This avoids paid API dependencies while preserving a provider-shaped boundary for later replacement.

## D006 — Kokoro-82M for voice
All listening and examiner speech is generated locally with Kokoro-82M ONNX. Audio assets are committed; the model and Python environment are gitignored.

## D007 — Demo bypass is not a security setting
`LOCAL_DEMO_MODE` is checked at API startup and refuses to run when `APP_ENV=production`. It is never enabled by the browser or by a request header.

## D008 — Cambridge pack is private local data
The repository now contains a four-test Cambridge IELTS 21 Academic pack supplied by the user. The source PDF prohibits redistribution without permission. The pack is treated as private local test data; public deployment requires rights clearance. See `extraction-report.md`.

## D009 — Share links are ephemeral quick tunnels
The showcase link is created on demand with an account-free Cloudflare quick tunnel to the local Next.js server. Tunnel start/stop is restricted to a loopback page; the public endpoint is read-only. The tunnel is killed when sharing stops or the API shuts down, so there is no long-lived public URL to secure or maintain.
