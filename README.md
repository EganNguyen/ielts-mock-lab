# Apex IELTS — Academic Mock Simulator

A local-first IELTS Academic computer-delivered simulation with all four skills. The app is designed around one rule: **the examination engine is deterministic, and no answer key reaches the browser before submission.**

## Status

| Area | State |
|---|---|
| Listening | 8 tests × 4 parts × 40 questions · one-play Kokoro audio |
| Reading | 8 tests × 3 passages × 40 questions · split-screen reader |
| Writing | 8 tests × Task 1 figure + Task 2 essay · word counts |
| Speaking | 8 tests × examiner-led Parts 1–3 · Kokoro voice · recording |
| Timing | Server-owned deadlines, refresh recovery, auto-close |
| Storage | PostgreSQL attempts, answers, immutable section snapshots, results |
| Scoring | Deterministic L/R conversion; local Writing/Speaking estimates |
| Local demo | No login required; demo bypass only when `LOCAL_DEMO_MODE=true` |
| Share link | Temporary public Cloudflare tunnel for a private showcase |
| Tests | Go unit tests + 8 Playwright end-to-end tests |

The local seed contains eight Academic tests: Cambridge IELTS 21 Tests 1–4 and IELTS 20 Tests 1–4. Both source PDFs carry copyright notices; treat the content as private local test data and confirm your rights before redistributing.

## Quick start

Requirements: Docker Desktop, Go 1.24+, Node.js 22+, pnpm.

```bash
cd /path/to/ielts-mock-lab
./scripts/dev.sh
```

This runs PostgreSQL in Docker, starts the Go API on `127.0.0.1:8080`, starts Next.js on `127.0.0.1:3000`, verifies the demo session and exam list, and opens the browser.

- App: <http://127.0.0.1:3000>
- API health: <http://127.0.0.1:8080/api/v1/health>
- Demo user: `demo@apex.local` (created automatically, no login prompt in demo mode)

Stop with `./scripts/stop.sh` — the PostgreSQL volume is preserved.

### Manual startup

```bash
docker compose up -d postgres
cd services/api
LOCAL_DEMO_MODE=true \
DATABASE_URL='postgres://apex:apex@127.0.0.1:5433/apex?sslmode=disable' \
go run ./cmd/api

# in another terminal
pnpm --dir apps/web dev
```

Migrations and seeds run automatically on API startup. They are idempotent and do not modify existing attempts.

## Local demo mode and security

`LOCAL_DEMO_MODE=true` makes the API resolve the seeded demo candidate when no session cookie exists. It is deliberately scoped:

- `APP_ENV=production` with `LOCAL_DEMO_MODE=true` makes the process **refuse to start**.
- In non-demo mode, `/auth/me`, attempts, answers, results and history require a valid HttpOnly session cookie.
- Registration/login/logout/me endpoints are implemented with bcrypt password hashes and hashed server-side sessions.
- Answer keys, transcripts and writing model answers are stripped from the public exam endpoint.
- Answer keys are only returned by `/attempts/{id}/review` after the attempt is completed.

Verified production guard:

```text
APP_ENV=production LOCAL_DEMO_MODE=true ./apex-api
exit=1
refusing to start: LOCAL_DEMO_MODE cannot be enabled in production
```

## Share a showcase link

The dashboard header has a **Share** button. Choose **Generate public link** and the API starts a Cloudflare quick tunnel to the local Next.js server. The dialog shows the public URL with copy, native device-share and stop controls.

![Share showcase dialog](docs/screenshots/share-link.png)

The same workflow is available from a terminal:

```bash
./scripts/share.sh          # start a tunnel and copy the link
./scripts/share.sh status   # show the current link
./scripts/share.sh stop     # close the tunnel
```

Requirements:

- `cloudflared` on `PATH` (`brew install cloudflared`)
- outbound internet access from the host
- the local app and the Mac must stay awake and running

The URL is random, temporary and requires no Cloudflare account. Tunnel start/stop requests are accepted only from the local page; a visitor opening the public URL cannot create or close it. The API stops the tunnel when it shuts down. While sharing, the friend sees the same demo candidate, so finish or discard any attempt in progress first. The four-test content pack is private local test data — share the link only with people you trust, not publicly.

For a **permanent** URL such as `https://ielts.your-domain.com`, set up a Cloudflare named tunnel and (recommended) Cloudflare Access email protection. See [docs/STATIC_LINK.md](docs/STATIC_LINK.md).

## Stack

- **Web:** Next.js 15 App Router, React 19, TypeScript, custom CSS.
- **API:** Go 1.24, `net/http`, `pgx/v5`.
- **Database:** PostgreSQL 16 in Docker.
- **Audio:** Kokoro-82M ONNX (local, free, no API keys) for all listening and examiner voice assets.
- **Transcription:** browser SpeechRecognition where available; clearly optional and never required.
- **Evaluation:** deterministic local rubric provider (`local-rubric-v1`) for Writing and Speaking. It is not an official IELTS examiner.
- **Tests:** Go testing + Playwright.

## Exam content

The content source of truth is `content/academic/`. The Go API embeds the Cambridge pack from `services/api/internal/content/`. Figures and Kokoro audio live under `apps/web/public/media/`. To rebuild the legacy typed content export:

```bash
node --experimental-strip-types scripts/export-content.mjs
```

The API validates the 4/3/2/3 section structure at startup. To import another book or add a test, follow the step-by-step [Extraction & Import Guide](docs/EXTRACTION_GUIDE.md). Both packs have been audited against their books — see the [Content Fidelity Report](docs/FIDELITY_REPORT.md) and the [IELTS 20 pack notes](docs/IELTS20.md).

### Kokoro voice assets

Listening is split into `part1.mp3` … `part4.mp3` under
`public/media/listening/<exam-id>/`; examiner prompts live under
`public/media/speaking/examiner/<exam-id>/`. They were generated with Kokoro-82M ONNX
using British voices (`bm_george`, `bm_lewis`, `bm_fable`, `bf_emma`, `bf_alice`, `bf_isabella`, `bf_lily`).

Regeneration requires the model files in `models/kokoro/` (gitignored):

```bash
uv venv --python 3.12 .venv-kokoro
source .venv-kokoro/bin/activate
uv pip install kokoro-onnx soundfile
# download kokoro-v1.0.onnx and voices-v1.0.bin into models/kokoro/
.venv-kokoro/bin/python content/cambridge21/tools/generate_audio.py
.venv-kokoro/bin/python content/cambridge21/tools/generate_speaking.py
```

The generated MP3s are committed, so normal local use needs neither the model nor Python.
See the [Extraction & Import Guide](docs/EXTRACTION_GUIDE.md) for the full pipeline.

## Commands

```bash
./scripts/dev.sh                 # start everything and open browser
./scripts/stop.sh                # stop API, web and PostgreSQL
./scripts/share.sh               # create a temporary public showcase link
./scripts/share.sh stop          # close the share link
pnpm --dir apps/web build        # production build
bash scripts/export-static.sh    # static export → apps/web/out (no API)
cd services/api && go test ./... # unit tests
cd apps/web && pnpm exec playwright test  # E2E (requires running app)
```

## Static / GitHub Pages mode

The lab can run without the Go API or PostgreSQL. In static mode the browser fetches
the eight exam JSON files from `public/data/exams`, saves attempts in `localStorage`,
and scores Listening/Reading locally.

```bash
bash scripts/export-static.sh
# artifact: apps/web/out
# preview: python3 -m http.server 4173 --directory apps/web/.static-preview
# then open http://127.0.0.1:4173/ielts-mock-lab/
```

`BASE_PATH` defaults to `/ielts-mock-lab` and must match the Pages project path.
The included workflow `.github/workflows/pages.yml` is manual (`workflow_dispatch`)
and uploads `apps/web/out` to Pages. Enable **Settings → Pages → Build and deployment
→ GitHub Actions** before running it.

Static mode has no server, tunnel, or durable storage: attempts live in that browser
only, share links are disabled, and Speaking recordings are not uploaded. Writing and
Speaking scores remain local estimates. Do **not** publish the site publicly unless you
have confirmed redistribution rights for the book content.

## Test evidence

Latest local run:

- `go test ./...` — **pass** (`internal/content`, `internal/scoring`).
- Playwright — **8/8 pass**:
  1. demo candidate sees exam without login;
  2. answers and one-play audio survive refresh;
  3. answer keys are absent before submission;
  4. full four-section attempt produces a persisted result report;
  5. Kokoro listening/examiner assets are served locally;
  6. dashboard exposes both exam packs and the share dialog.
- Browser walkthrough: full mock started, Listening → Reading → Writing → Speaking completed, results generated, page refreshed and result persisted.
- Production guard: demo bypass refused with `APP_ENV=production`.

## Known limitations

- Writing and Speaking scores are **local estimates**, not official IELTS examiner results.
- Speaking transcription depends on browser SpeechRecognition support; recordings and duration are still saved without it.
- The seed contains eight Academic tests (Cambridge IELTS 21 and IELTS 20). The source PDFs prohibit redistribution without permission; confirm your rights before publishing this content. See `extraction-report.md`.
- Listening audio is Kokoro-generated for each test under `apps/web/public/media/listening/<exam-id>/`. The section clock remains 30 minutes as in the exam specification.
- No admin content editor UI yet. Content changes are made through the versioned JSON + reseed workflow.

## Repository map

```
apps/web/                 Next.js candidate app
  app/                    dashboard, exam runner, results
  src/components/exam/    question renderer, speaking room
  public/media/           Kokoro audio assets
services/api/             Go API, exam engine, scoring
  internal/db/            PostgreSQL store + migrations
  internal/scoring/       deterministic and rubric scoring
  internal/content/       embedded content seed
content/academic/         content source JSON
docs/                     architecture, scoring, API, test strategy
scripts/                  export, audio generation, local startup
```
