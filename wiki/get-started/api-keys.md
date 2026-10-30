# Get an API key

Every request under `/v1` needs an API key in the `X-API-Key` header. Keys
look like `pk_` followed by 48 hex characters.

## Request a key

There's no sign-up page yet. Keys are issued by the API owner.

1. **[Open a key request]({{ key_request_url }})** (a GitHub issue).
2. Say:
    - **App name**: what's calling the API, e.g. `pill-identifier-web`.
    - **Where it runs**: in a browser (list your site's origins, such as
      `https://myapp.example.com`) or on a server or script (no origins needed).
    - **Expected traffic**: roughly how many requests per minute at peak.
3. You'll get back your key, its **rate limit** and its **allowed origins**.

!!! warning "Treat the key like a password"
    Don't commit it to git or paste it in issues or chat. On a server, load it
    from an environment variable or secret store. In a browser it is visible to
    users, which is why browser keys are locked to your origins.

## What you receive

| Field | Meaning |
|---|---|
| `key` | Your API key, sent as `X-API-Key` |
| `rate_limit` | Requests allowed per minute (sliding window) for this key |
| `origins` | Websites allowed to call the API from a browser with this key |
| `active` | Whether the key works |

## Using the key from a browser vs a server

- **Server, script or mobile backend:** no `Origin` header is sent, so the
  origins list doesn't apply. Just send the key.
- **Browser (fetch/XHR from a web page):** the API only adds the CORS header for
  origins on your key's list. Any other site's request is blocked **by the
  browser** with a CORS error. The API doesn't return 403 for this. A key with
  no origins can't be used from a browser at all. A key with `*` works from any site.

## Rate limits

Each key has its own limit in requests per minute. Every response tells you
where you stand, through the `X-RateLimit-Limit`, `X-RateLimit-Remaining` and
`X-RateLimit-Reset` headers. Over the limit you get `429` with a `Retry-After`
header. See [Errors and rate limits](../reference/errors.md#rate-limits).

## Rotate or replace a key

- **Rotate** (planned change, e.g. a key was exposed): ask for a rotation. You
  get a new key, and the old one keeps working for a grace period (for example
  24h) so you can switch without downtime.
- **Lost key:** keys can't be looked up by users. Ask for a new key; the old
  one is deactivated.

## For admins: issuing a key

Keys are created through the admin API with the admin bearer secret. The secret
is never shared with API users.

```bash
curl -X POST {{ api_base }}/admin/keys \
  -H "Authorization: Bearer $ADMIN_SECRET" \
  -H "Content-Type: application/json" \
  -d '{"app_name": "pill-identifier-web", "origins": ["https://myapp.example.com"], "rate_limit": 250}'
```

```json
{
  "key": "pk_…",
  "app_name": "pill-identifier-web",
  "origins": ["https://myapp.example.com"],
  "rate_limit": 250,
  "active": true,
  "created_at": "2026-10-30T14:37:37.020881Z"
}
```

Rules: `app_name` is required; `rate_limit` must be 1–10000; at most 20
origins. Other admin operations (all under `/admin/keys`):

| Action | Request |
|---|---|
| List keys | `GET /admin/keys` |
| Show one key | `GET /admin/keys/{key}` |
| Deactivate | `DELETE /admin/keys/{key}` |
| Rotate with grace period | `POST /admin/keys/{key}/rotate` with `{"grace_period": "24h"}` |
