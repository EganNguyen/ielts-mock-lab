# Agent Instructions — Apex IELTS

If the user says **“run this project”**, start the local app and verify it. Do not modify content or architecture unless asked.

## TL;DR

```bash
cd /path/to/ielts-mock-lab
bash scripts/dev.sh
bash scripts/verify.sh
```

Then open **http://127.0.0.1:3000**.

The app runs in **local demo mode**: no registration, no login, no API keys. Eight Academic tests are seeded — Cambridge IELTS 21 Tests 1–4 and IELTS 20 Tests 1–4 — each with 40 Listening, 40 Reading, 2 Writing and 3 Speaking parts.

## Prerequisites

| Dependency | Required | macOS install |
|---|---|---|
| Docker Desktop | PostgreSQL container | `brew install --cask docker` then launch Docker |
| Go | 1.24+ | `brew install go` |
| Node.js | 22+ | `brew install node` |
| pnpm | 11.x | `npm install -g pnpm@11` |
| curl | health checks | preinstalled on macOS |

Linux/WSL: install Go, Node, pnpm, Docker Engine + Compose, then run the same script. The script starts Docker Desktop automatically only on macOS.

## New machine — agent runbook

When the user says **“run this project”** on a fresh machine:

1. Read this file and `README.md`.
2. Check `docker`, `go`, `node`, `pnpm`, `curl`.
3. On macOS, install missing tools with:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   brew install --cask docker
   brew install go node pnpm
   open -a Docker
   ```
   Wait for Docker Desktop to finish starting. The free Docker Desktop licence prompt is the only manual GUI step; do not ask the user for API keys.
4. Run from the repository root:
   ```bash
   bash scripts/dev.sh
   bash scripts/verify.sh
   ```
5. Report the URL and verification result. Do not ask the user to configure `.env`; local defaults are built into the script.
6. If the user wants to stop it: `bash scripts/stop.sh`.

No registration, login, paid AI key, Kokoro model download, or manual database migration is required on the new machine. The audio files are committed.

## What `scripts/dev.sh` does

1. Checks prerequisites and starts Docker Desktop if needed on macOS.
2. Starts PostgreSQL via `docker compose up -d postgres` on port **5433**.
3. Installs web dependencies with `pnpm install` if `node_modules` is missing.
4. Starts the Go API on **127.0.0.1:8080**, with:
   - `LOCAL_DEMO_MODE=true`
   - `APP_ENV=development`
   - PostgreSQL migrations + idempotent exam seed
5. Starts Next.js on **127.0.0.1:3000**.
6. Verifies the demo candidate, eight-exam list, audio assets and web page.
7. Opens the browser on macOS.

Logs:

- API: `/tmp/apex-api.log`
- Web: `/tmp/apex-web.log`

Stop:

```bash
bash scripts/stop.sh
```

The PostgreSQL volume is preserved. Attempts are **not** deleted by stopping.

## Verification

```bash
bash scripts/verify.sh
```

Expected output includes:

```text
"database":true
"demoMode":true
"speechProvider":"kokoro-82m-onnx"
PASS: web, API, database, demo candidate, both exam packs' audio, figures and Kokoro assets are healthy.
```

Expected URLs:

- App: <http://127.0.0.1:3000>
- API health: <http://127.0.0.1:8080/api/v1/health>
- Exam list through web proxy: <http://127.0.0.1:3000/api/v1/exams>

## Trigger phrase

If the user says **“extract this pdf for ielts mock test”** (or similar) and provides a
PDF, follow `docs/EXTRACTION_GUIDE.md` end to end: derive the pack name, extract all four
tests plus keys/transcripts/figures, build content, generate audio, reseed, run the four
gates, and report coverage/fixes. Ask only for a missing PDF path or rights confirmation.

## Important rules

- **Do not add more Cambridge content without permission.** The existing eight-test library is private local test data; both source PDFs prohibit redistribution. Read `extraction-report.md`.
- Do not run `pnpm build` or `pnpm --dir apps/web build` while the Next dev server is running. It rewrites `.next` and can break the dev server. Stop the web server first if a production build is required.
- Do not delete `docker compose` volume `apex_pgdata` unless the user explicitly asks to reset all attempts.
- Do not enable `LOCAL_DEMO_MODE=true` with `APP_ENV=production`. The API refuses to start in that combination.
- Answer keys must never be exposed before an attempt is completed. Keep the public/review payload separation in `services/api/internal/model/model.go`.
- Kokoro audio is committed under `apps/web/public/media/`. The Kokoro model and Python environment are only needed to regenerate audio, not to run the app.
- When asked to extract or import another book/test, follow [`docs/EXTRACTION_GUIDE.md`](docs/EXTRACTION_GUIDE.md) end to end and run its four gates.

## Useful commands

```bash
# full local stack
bash scripts/dev.sh

# stop API, web and PostgreSQL
bash scripts/stop.sh

# verify running services
bash scripts/verify.sh

# API tests
cd services/api && go test ./...

# Playwright tests (requires running app)
cd apps/web && pnpm exec playwright test

# production web build (stop dev web first)
cd apps/web && pnpm build

# rebuild content JSON after editing typed content
node --experimental-strip-types scripts/export-content.mjs
```

## Troubleshooting

| Symptom | Fix |
|---|---|
| `Cannot connect to the Docker daemon` | Launch Docker Desktop; rerun `scripts/dev.sh`. |
| `port 8080 is already in use` | `lsof -ti tcp:8080 \| xargs kill` then rerun. |
| `Port 3000 is occupied` | Stop the other Next/Vite app; rerun. |
| Web page loads but buttons do nothing | The dev server was corrupted by a concurrent `next build`. Kill port 3000, delete `apps/web/.next`, restart. |
| API starts but DB errors | `docker compose up -d postgres`; wait for healthy; check `/tmp/apex-api.log`. |
| Audio does not play | Click the “Play exam audio” overlay; browsers may block autoplay. Kokoro assets are local under `apps/web/public/media/listening/<exam-id>/`. |
| Speaking page asks for microphone | Allow the microphone. Without it, use “Continue without recording”; the estimate is labelled accordingly. |

## Current state

- Eight Academic tests are seeded: Cambridge IELTS 21 Tests 1–4 and IELTS 20 Tests 1–4.
- Each test has 40 Listening, 40 Reading, 2 Writing and 3 Speaking parts.
- Writing Task 1 figures and listening maps are stored under `apps/web/public/media/figures/<pack>/`.
- Listening audio is under `apps/web/public/media/listening/<exam-id>/`.
- Local demo access without login.
- Kokoro-82M voice for listening and examiner prompts.
- Go + PostgreSQL persistence, server-owned timers, autosave, refresh recovery.
- Results and answer review; writing/speaking scores are local estimates, not official IELTS scores.

## Content provenance

The tests were authored from the user-provided Cambridge IELTS 21 and IELTS 20 PDF packs. Both books carry copyright notices prohibiting reproduction without permission. Treat this content as **private local test data**; do not redistribute the repository publicly without confirming rights. See `extraction-report.md` and `docs/IELTS20.md`.
