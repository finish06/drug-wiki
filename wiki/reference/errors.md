# Errors and rate limits

## Error format

Every error is JSON with a machine-readable code and a human message:

```json
{ "error": "bad_request", "message": "Either 'name' or 'ndc' query parameter is required" }
```

Branch on the HTTP status and `error`; show `message` to developers, not end users.

## Status codes

| Status | `error` | What happened | What to do |
|---|---|---|---|
| 200 | — | Success. Lists may be empty | Handle empty lists and `null` objects |
| 400 | `bad_request` | A parameter is missing or invalid | Fix the request; the message names the parameter |
| 401 | `unauthorized` | `API key required` or `Invalid API key` | Send a valid `X-API-Key` |
| 403 | — | Not returned for API calls. A browser request from an origin not on your key fails as a **CORS error** in the browser instead | Ask for your origin to be added to the key |
| 404 | `not_found` | No drug, label or concept for that identifier | Treat as "no result"; check the ID format |
| 429 | `rate_limited` | Over your key's per-minute limit | Wait `Retry-After` seconds, then retry |
| 500 | `internal_error` | Unexpected server error | Retry once; report it if it persists |
| 502 | `upstream_error` | A data source (DailyMed, FDA, RxNorm) failed or timed out, and no cached copy was available | Retry with backoff (e.g. 1s, 2s, 4s) |

## Rate limits

Each key allows a fixed number of requests per minute, counted over a sliding
60-second window. Every authenticated response includes:

| Header | Meaning |
|---|---|
| `X-RateLimit-Limit` | Requests allowed per minute for your key |
| `X-RateLimit-Remaining` | Requests left in the current window |
| `X-RateLimit-Reset` | Unix time when the window fully resets |
| `Retry-After` | On `429` only: seconds to wait |

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 60
X-RateLimit-Limit: 250
X-RateLimit-Remaining: 0

{"error":"rate_limited","message":"Rate limit exceeded"}
```

Good habits:

- Cache results on your side. Drug data changes slowly.
- Debounce autocomplete keystrokes.
- Need a higher limit? Ask for it ([API keys](../get-started/api-keys.md)).
