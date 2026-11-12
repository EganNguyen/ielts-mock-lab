#!/usr/bin/env bash
set -euo pipefail
WEB="http://127.0.0.1:3000"
API="http://127.0.0.1:8080"

fail() { echo "FAIL: $*" >&2; exit 1; }

health="$(curl -fsS "$API/api/v1/health")" || fail "API health endpoint is not reachable"
echo "API health: $health"
echo "$health" | grep -q '"database":true' || fail "PostgreSQL ping failed"
echo "$health" | grep -q '"demoMode":true' || fail "LOCAL_DEMO_MODE is not enabled"
echo "$health" | grep -q 'kokoro-82m-onnx' || fail "Kokoro speech provider is not active"

exams="$(curl -fsS "$WEB/api/v1/exams")" || fail "Exam list is not reachable through the web proxy"
echo "$exams" | grep -q '"id":"cambridge21-test1"' || fail "Seeded Cambridge 21 test 1 is missing"
echo "$exams" | grep -q '"id":"cambridge21-test4"' || fail "Seeded Cambridge 21 test 4 is missing"
echo "$exams" | grep -q '"id":"ielts20-test1"' || fail "Seeded IELTS 20 test 1 is missing"
echo "$exams" | grep -q '"id":"ielts20-test4"' || fail "Seeded IELTS 20 test 4 is missing"
me="$(curl -fsS "$WEB/api/v1/auth/me")" || fail "Demo candidate endpoint failed"
echo "$me" | grep -q 'demo@apex.local' || fail "Demo candidate was not resolved"
share="$(curl -fsS "$WEB/api/v1/share")" || fail "Share status endpoint failed"
echo "$share" | grep -q 'cloudflare-quick-tunnel' || fail "Share provider is not wired up"
curl -fsS "$WEB/" | grep -qi 'apex' || fail "Web app is not serving Apex IELTS"

# Every seeded pack must have candidate audio and, where applicable, figures.
for pack in cambridge21 ielts20; do
  for test in 1 2 3 4; do
    for part in 1 2 3 4; do
      code="$(curl -s -o /dev/null -w '%{http_code}' "$WEB/media/listening/$pack-test$test/part$part.mp3")"
      [[ "$code" == "200" || "$code" == "206" ]] || fail "$pack test$test listening part$part returned HTTP $code"
    done
  done
  for figure in test1-writing-task1.jpg test2-writing-task1.jpg test3-writing-task1.jpg test4-writing-task1.jpg; do
    code="$(curl -s -o /dev/null -w '%{http_code}' "$WEB/media/figures/$pack/$figure")"
    [[ "$code" == "200" ]] || fail "$pack figure $figure returned HTTP $code"
  done
  if [[ "$pack" == "cambridge21" ]]; then
    code="$(curl -s -o /dev/null -w '%{http_code}' "$WEB/media/figures/$pack/test2-listening-map.jpg")"
    [[ "$code" == "200" ]] || fail "$pack listening map returned HTTP $code"
  else
    code="$(curl -s -o /dev/null -w '%{http_code}' "$WEB/media/figures/$pack/test3-listening-map.jpg")"
    [[ "$code" == "200" ]] || fail "$pack listening map returned HTTP $code"
  fi
  for test in 1 2 3 4; do
    for asset in "intro" "cue" "s1" "s10"; do
      path="/media/speaking/examiner/$pack-test$test/$asset.mp3"
      code="$(curl -s -o /dev/null -w '%{http_code}' "$WEB$path")"
      [[ "$code" == "200" || "$code" == "206" ]] || fail "$path returned HTTP $code"
    done
  done
done
echo "PASS: web, API, database, demo candidate, both exam packs' audio, figures and Kokoro assets are healthy."
