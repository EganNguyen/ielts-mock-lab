#!/usr/bin/env bash
# Create or stop the temporary public link for the local showcase.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

WEB="${WEB_URL:-http://127.0.0.1:3000}"
API="${API_URL:-http://127.0.0.1:8080}"
ORIGIN="$WEB"
ACTION="${1:-start}"

say() { printf '\033[1;32m[share]\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33m[share]\033[0m %s\n' "$*"; }
fail() { printf '\033[1;31m[share]\033[0m %s\n' "$*" >&2; exit 1; }

need_app() {
  curl -fsS "$API/api/v1/health" >/dev/null 2>&1 \
    || fail "The local API is not running. Start it with ./scripts/dev.sh first."
  curl -fsS "$WEB" >/dev/null 2>&1 \
    || fail "The local website is not running at $WEB. Start it with ./scripts/dev.sh first."
}

copy_link() {
  local url="$1"
  if [[ "$(uname -s)" == "Darwin" ]] && command -v pbcopy >/dev/null; then
    printf '%s' "$url" | pbcopy && say "Link copied to the clipboard."
  elif command -v wl-copy >/dev/null; then
    printf '%s' "$url" | wl-copy && say "Link copied to the clipboard."
  elif command -v xclip >/dev/null; then
    printf '%s' "$url" | xclip -selection clipboard && say "Link copied to the clipboard."
  fi
}

status() {
  local json
  json="$(curl -fsS "$API/api/v1/share")" || fail "Could not read the share status."
  local url active available message
  url="$(printf '%s' "$json" | sed -n 's/.*"url":"\([^"]*\)".*/\1/p')"
  active="$(printf '%s' "$json" | sed -n 's/.*"active":\([a-z]*\).*/\1/p')"
  available="$(printf '%s' "$json" | sed -n 's/.*"available":\([a-z]*\).*/\1/p')"
  message="$(printf '%s' "$json" | sed -n 's/.*"message":"\([^"]*\)".*/\1/p')"
  if [[ "$active" == "true" && -n "$url" ]]; then
    say "Sharing: $url"
  else
    say "No active share link."
    if [[ "$available" == "false" ]]; then
      warn "cloudflared was not found on PATH. Install it with: brew install cloudflared"
    elif [[ -n "$message" && "$message" != "The share link was stopped" ]]; then
      warn "$message"
    fi
  fi
  return 0
}

start() {
  need_app
  command -v cloudflared >/dev/null \
    || fail "cloudflared is required. Install it with: brew install cloudflared"

  say "Opening a Cloudflare quick tunnel… this can take a few seconds."
  local json
  json="$(curl -sS -X POST \
    -H "Origin: $ORIGIN" \
    -H 'Content-Type: application/json' \
    --data '{}' \
    "$API/api/v1/share")" || fail "The share request failed: $json"

  local url
  url="$(printf '%s' "$json" | sed -n 's/.*"url":"\([^"]*\)".*/\1/p')"
  if [[ -z "$url" ]]; then
    fail "Could not create a link. Server response: $json"
  fi

  say "Public showcase: $url"
  copy_link "$url"
  say "Keep this Mac and the local app running. Stop with: ./scripts/share.sh stop"
}

stop() {
  local json
  json="$(curl -sS -X DELETE -H "Origin: $ORIGIN" "$API/api/v1/share")" \
    || fail "The stop request failed: $json"
  say "Share link stopped."
}

case "$ACTION" in
  start) start ;;
  stop | --stop) stop ;;
  status) status ;;
  *)
    echo "Usage: $0 [start|stop|status]" >&2
    exit 2
    ;;
esac
