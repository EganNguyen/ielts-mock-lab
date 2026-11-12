#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
if [[ -f /tmp/apex-ielts-dev.pids ]]; then
  while read -r pid; do [[ -n "${pid:-}" ]] && kill "$pid" 2>/dev/null || true; done < /tmp/apex-ielts-dev.pids
  rm -f /tmp/apex-ielts-dev.pids
fi
lsof -ti tcp:8080 | xargs -r kill 2>/dev/null || true
lsof -ti tcp:3000 | xargs -r kill 2>/dev/null || true
docker compose stop postgres >/dev/null 2>&1 || true
echo "Stopped Apex IELTS (database volume preserved)."
