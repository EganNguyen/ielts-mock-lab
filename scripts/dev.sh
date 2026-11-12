#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
PIDFILE="/tmp/apex-ielts-dev.pids"
: > "$PIDFILE"

log() { printf '\n\033[1;32m[apex]\033[0m %s\n' "$*"; }
warn() { printf '\n\033[1;33m[apex]\033[0m %s\n' "$*"; }

missing() {
  echo "Missing dependency: $1" >&2
  echo "$2" >&2
  exit 1
}

# 0. Prerequisites ------------------------------------------------------------
command -v docker >/dev/null || missing "docker" "Install Docker Desktop: https://www.docker.com/products/docker-desktop/"
command -v curl >/dev/null || missing "curl" "Install curl with your system package manager."
command -v go >/dev/null || missing "go" "Install Go 1.24+: brew install go (macOS) or https://go.dev/dl/"
command -v node >/dev/null || missing "node" "Install Node.js 22+: brew install node (macOS) or https://nodejs.org/"
if ! command -v pnpm >/dev/null; then
  if command -v corepack >/dev/null; then
    warn "pnpm not found; enabling via corepack…"
    corepack enable >/dev/null 2>&1 || true
    corepack prepare pnpm@11.9.0 --activate >/dev/null 2>&1 || true
  fi
fi
command -v pnpm >/dev/null || missing "pnpm" "Install pnpm: npm install -g pnpm@11"

# 1. Local infrastructure -----------------------------------------------------
if ! docker info >/dev/null 2>&1; then
  if [[ "$(uname -s)" == "Darwin" ]]; then
    warn "Docker Desktop is not running. Starting it…"
    open -a Docker || true
    for _ in $(seq 1 60); do docker info >/dev/null 2>&1 && break; sleep 2; done
  fi
fi
if ! docker info >/dev/null 2>&1; then
  echo "Docker is required for PostgreSQL. Start Docker Desktop and retry." >&2
  exit 1
fi
log "Ensuring PostgreSQL is running…"
docker compose up -d postgres
for _ in $(seq 1 40); do
  docker compose exec -T postgres pg_isready -U apex -d apex >/dev/null 2>&1 && break
  sleep 1
done
docker compose exec -T postgres pg_isready -U apex -d apex >/dev/null

# 2. Dependencies -------------------------------------------------------------
if [[ ! -d apps/web/node_modules/next ]]; then
  log "Installing web dependencies…"
  pnpm install
fi
if ! command -v go >/dev/null; then
  echo "Go 1.24+ is required. Install Go and retry." >&2
  exit 1
fi

# 3. API ----------------------------------------------------------------------
API_HEALTH="http://127.0.0.1:8080/api/v1/health"
API_ALREADY=0
for _ in $(seq 1 10); do
  if curl -fsS "$API_HEALTH" >/dev/null 2>&1; then API_ALREADY=1; break; fi
  sleep 1
done
if [[ "$API_ALREADY" == "1" ]]; then
  log "Apex API is already running on :8080"
else
  if lsof -ti tcp:8080 >/dev/null 2>&1; then
    echo "Port 8080 is occupied but the Apex health endpoint is not responding." >&2
    exit 1
  fi
  log "Starting Go API on :8080…"
  (
    cd services/api
    LOCAL_DEMO_MODE=true \
    APP_ENV=development \
    DATABASE_URL='postgres://apex:apex@127.0.0.1:5433/apex?sslmode=disable' \
    MEDIA_DIR='./media' \
    WEB_ORIGIN='http://127.0.0.1:3000' \
    SHARE_TARGET='http://127.0.0.1:3000' \
    go run ./cmd/api > /tmp/apex-api.log 2>&1 &
    echo $! >> "$PIDFILE"
  )
  for _ in $(seq 1 60); do
    curl -fsS "$API_HEALTH" >/dev/null 2>&1 && break
    sleep 1
  done
fi
if ! curl -fsS "$API_HEALTH" >/dev/null 2>&1; then
  echo "API failed to start. Last log lines:" >&2
  tail -40 /tmp/apex-api.log >&2 || true
  exit 1
fi
log "API health: $(curl -fsS "$API_HEALTH")"

# 4. Web ----------------------------------------------------------------------
WEB_URL="http://127.0.0.1:3000"
WEB_ALREADY=0
for _ in $(seq 1 10); do
  if curl -fsS "$WEB_URL" 2>/dev/null | grep -qi 'apex'; then WEB_ALREADY=1; break; fi
  sleep 1
done
if [[ "$WEB_ALREADY" == "1" ]]; then
  log "Next.js is already running at $WEB_URL"
else
  if lsof -ti tcp:3000 >/dev/null 2>&1; then
    echo "Port 3000 is occupied by another process. Stop it or set a different web port." >&2
    exit 1
  fi
  log "Starting Next.js on :3000…"
  (pnpm --dir apps/web dev > /tmp/apex-web.log 2>&1 & echo $! >> "$PIDFILE")
  for _ in $(seq 1 60); do
    curl -fsS "$WEB_URL" >/dev/null 2>&1 && break
    sleep 1
  done
fi
if ! curl -fsS "$WEB_URL" 2>/dev/null | grep -qi 'apex'; then
  echo "Web app failed to start. Last log lines:" >&2
  tail -40 /tmp/apex-web.log >&2 || true
  exit 1
fi

# 5. Verify the exam list and demo session -----------------------------------
log "Verifying demo session and exam list…"
exams_json="$(curl -fsS "$WEB_URL/api/v1/exams")"
grep -q 'cambridge21-test1' <<<"$exams_json"
grep -q 'ielts20-test1' <<<"$exams_json"
log "Demo candidate: $(curl -fsS "$WEB_URL/api/v1/auth/me" | head -c 180)"
if [[ -x "$ROOT/scripts/verify.sh" ]]; then
  bash "$ROOT/scripts/verify.sh"
fi

log "Ready: $WEB_URL"
log "Logs: /tmp/apex-api.log · /tmp/apex-web.log"
log "Stop with: ./scripts/stop.sh"
if [[ "$(uname -s)" == "Darwin" ]]; then open "$WEB_URL"; fi
