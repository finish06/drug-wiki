# Read product labels (SPL)

Every US drug product has an official FDA label, published on DailyMed as a
**Structured Product Label (SPL)**. Search a drug's labels, then fetch one with
its parsed sections.

## When to use

- Show *all* labels for a drug (several manufacturers, repackagers, versions).
- Show a specific label a user picked, or the one behind an
  [interaction match](interactions.md) (`spl_setid`).

For "just tell me about this drug", the [info card](drug-info.md) is simpler.
It picks the newest label for you.

## Request

```bash
# search labels by drug name (paginated)
curl -s "{{ api_base }}/v1/drugs/spls?name=warfarin&limit=3" -H "X-API-Key: $DRUG_API_KEY"

# one label by set ID, with parsed sections
curl -s "{{ api_base }}/v1/drugs/spls/8ad881e0-ca41-42ad-9d7d-eb85b3a30af0" -H "X-API-Key: $DRUG_API_KEY"
```

## Example response

Search (captured 2026-10-30):

```json
{
  "data": [
    { "title": "WARFARIN SODIUM TABLET [A-S MEDICATION SOLUTIONS]",
      "setid": "654ca5d2-d4c1-48f8-90c4-130a21162bb0",
      "published_date": "Sep 23, 2026", "spl_version": 9 }
  ],
  "pagination": { "page": 1, "limit": 3, "total": 117, "total_pages": 39 }
}
```

Detail returns the same fields plus `interactions`, `contraindications`,
`warnings` and `adverse_reactions` (lists of `{ "title", "text" }`), exactly as
in the [info card](drug-info.md#example-response).

!!! note "Dates"
    `published_date` is DailyMed's display format, `"Sep 23, 2026"`, not ISO 8601.
    Parse it before sorting: comparing the strings orders them by month
    name, not by date.

## Parameters

| Endpoint | Name | Required | Notes |
|---|---|---|---|
| `/spls` | `name` | yes | Drug name |
| `/spls` | `page`, `limit` | no | Default limit 20, max 100 |
| `/spls/{setid}` | `setid` | yes | Label set ID (a UUID) |

## Errors

| Status | `error` | Meaning |
|---|---|---|
| 400 | `bad_request` | `name` missing |
| 404 | `not_found` | No label with that set ID |
| 401 | `unauthorized` | Missing or invalid API key |
| 502 | `upstream_error` | DailyMed unreachable or throttling; retry |

## Related

- [Glossary: SPL, Set ID](../reference/glossary.md).
- Check several drugs' labels against each other: [Check drug interactions](interactions.md).
