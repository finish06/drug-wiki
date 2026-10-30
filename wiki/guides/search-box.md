# Build a drug search box

Suggest drug names as the user types, then let them pick one.

## When to use

| Need | Endpoint |
|---|---|
| Suggestions while typing (prefix match, very fast) | `GET /v1/drugs/autocomplete` |
| A full, filterable, paginated list of names | `GET /v1/drugs/names` |
| The user typed a misspelling ("lipitr") | [`GET /v1/drugs/rxnorm/search`](rxnorm.md) |

## Request

Call autocomplete once the user has typed **2 or more characters**, and debounce
keystrokes (about 150 ms) so you don't send a request per key.

```bash
curl -s "{{ api_base }}/v1/drugs/autocomplete?q=lipi&limit=5" -H "X-API-Key: $DRUG_API_KEY"
```

For a browsable list with filters:

```bash
curl -s "{{ api_base }}/v1/drugs/names?q=statin&type=generic&page=1&limit=50" -H "X-API-Key: $DRUG_API_KEY"
```

## Example response

Autocomplete:

```json
{
  "data": [
    { "name": "Lipitor", "type": "brand" },
    { "name": "Lipitor Pill", "type": "brand" }
  ]
}
```

Names listing:

```json
{
  "data": [
    { "name": "atorvastatin calcium", "type": "generic" }
  ],
  "pagination": { "page": 1, "limit": 50, "total": 1234, "total_pages": 25 }
}
```

*Shapes from the API's OpenAPI schema.*

## Parameters

**`/v1/drugs/autocomplete`**

| Name | Required | Notes |
|---|---|---|
| `q` | yes | Prefix, at least 2 characters, case-insensitive |
| `limit` | no | Default 10, max 50 |

**`/v1/drugs/names`**

| Name | Required | Notes |
|---|---|---|
| `q` | no | Substring filter, case-insensitive |
| `type` | no | `generic`, `brand` or `all` (default) |
| `page` | no | Default 1 |
| `limit` | no | Default 50, max 100 |

## Errors

| Status | `error` | Meaning |
|---|---|---|
| 400 | `bad_request` | `q` missing or shorter than 2 characters (autocomplete), or a bad `type`/`limit` |
| 401 | `unauthorized` | Missing or invalid API key |
| 429 | `rate_limited` | Too many keystroke requests. Debounce, and respect `Retry-After` |
| 502 | `upstream_error` | The names list couldn't be loaded; retry |

## Related

- Once the user picks a name: [Show a drug info card](drug-info.md) or [Browse by drug class](drug-classes.md).
- Misspellings and canonical IDs: [Normalize names with RxNorm](rxnorm.md).
