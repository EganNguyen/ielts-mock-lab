# API

Base: `/api/v1`

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Liveness, database ping, provider status |
| GET | `/config` | Demo/provider configuration |
| GET | `/auth/me` | Current candidate (demo or session) |
| POST | `/auth/register` | Create candidate |
| POST | `/auth/login` | Cookie session |
| POST | `/auth/logout` | Delete session |
| GET | `/share` | Current temporary showcase link status (public, read-only) |
| POST | `/share` | Start a Cloudflare quick tunnel (local page only) |
| DELETE | `/share` | Stop the quick tunnel (local page only) |
| GET | `/exams` | Published exams |
| GET | `/exams/{id}` | Public exam content (no keys) |
| POST | `/exams/{id}/attempts` | Create and start attempt |
| GET | `/attempts/active` | Latest in-progress attempt |
| GET | `/attempts/{id}` | State, public exam, saved answers |
| POST | `/attempts/{id}/sections/{skill}/start` | Start section |
| PUT | `/attempts/{id}/sections/{skill}/answers/{questionId}` | Save answer `{value,version}` |
| POST | `/attempts/{id}/sections/{skill}/submit` | Lock section + immutable snapshot |
| POST | `/attempts/{id}/speaking` | Multipart recording upload |
| POST | `/attempts/{id}/complete` | Generate result |
| GET | `/attempts/{id}/results` | Stored result |
| GET | `/attempts/{id}/review` | Completed-only report with keys |
| GET | `/history` | Completed attempt summaries |

Errors use `{"error":{"code":"...","message":"..."}}`.

`POST` and `DELETE /share` require a loopback `Origin` and reject requests that arrived through Cloudflare. `POST` is also refused outside local demo mode. The generated URL is a random `*.trycloudflare.com` hostname; shutting down the API tears the tunnel down.

Demo mode is process-wide and unavailable when `APP_ENV=production`.
