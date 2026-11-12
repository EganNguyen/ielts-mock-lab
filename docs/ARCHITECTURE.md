# Architecture

```
Browser (Next.js 15 / React 19)
  ├─ Dashboard / exam list
  ├─ /exam/[attemptId]  → section runner + autosave + recorder
  └─ /results/[id]      → report + answer review
        │  same-origin /api/v1/* and /media/* rewrites
        ▼
Go API (net/http, pgx/v5)
  ├─ demo/cookie auth
  ├─ exam + attempt lifecycle
  ├─ section deadlines and submissions
  ├─ answer validation and versions
  ├─ speaking upload → local media dir
  ├─ deterministic scoring + local rubric
  ├─ public vs review payload separation
  └─ share manager → cloudflared quick tunnel (local-control only)
        ▼
PostgreSQL 16
  users, sessions, exams, exam_versions, attempts,
  attempt_sections, answers, section_submissions,
  speaking_recordings, results, audit_logs
```

## Request flow
1. `POST /exams/{id}/attempts` creates an attempt and its section rows. The first section starts immediately.
2. The browser loads `GET /attempts/{id}`. Public exam content contains no answer keys.
3. Each answer is `PUT` with the client's known version. PostgreSQL row locking prevents lost updates.
4. `POST /sections/{skill}/submit` is idempotent, locks the section and writes an immutable snapshot.
5. After the final section, `POST /attempts/{id}/complete` computes the result and stores the full report in `results.details`.
6. `GET /attempts/{id}/review` is only available for completed attempts and returns keys, explanations, transcripts and model answers.

## Share flow
1. The local dashboard calls `POST /api/v1/share`; the API rejects the request unless it came from a loopback page (and never from a Cloudflare-proxied visit).
2. The share manager starts one `cloudflared tunnel --url http://127.0.0.1:3000 --no-autoupdate` process and parses its public hostname.
3. `GET /api/v1/share` is read-only and lets the dialog poll for the live URL. `DELETE` stops the process; API shutdown also stops it.
4. Visitors open the random public URL and use the same demo candidate; they cannot create or stop tunnels.

## Failure handling
- The API process runs migrations and seeds on startup. Migrations are idempotent.
- If the page is refreshed, attempt state, deadline, saved answers, flag state, and listening audio part/position are restored.
- Expired sections are marked `expired`; save requests are rejected.
- If a save receives a 409 conflict, the client refreshes attempt state.
- Audio is one-play: the hidden player has no seek/pause control, and the restored position requires an explicit user gesture.

## Local demo isolation
`LOCAL_DEMO_MODE` resolves the seeded demo candidate. It is checked at process start and refuses to run with `APP_ENV=production`. Normal cookie sessions remain available and are exercised in non-demo mode.
