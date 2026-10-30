# Browse by drug class

Find which classes a drug belongs to ("atorvastatin is an HMG-CoA reductase
inhibitor"), list the classes, or list the drugs in a class.

## When to use

| Need | Endpoint |
|---|---|
| Classes and brand names for one drug | `GET /v1/drugs/class?name=` |
| All classes, optionally by type | `GET /v1/drugs/classes` |
| Every drug in one class (alternatives, "other statins") | `GET /v1/drugs/classes/drugs?class=` |

## Request

```bash
curl -s "{{ api_base }}/v1/drugs/class?name=simvastatin" -H "X-API-Key: $DRUG_API_KEY"
curl -s "{{ api_base }}/v1/drugs/classes?type=epc&limit=3" -H "X-API-Key: $DRUG_API_KEY"
curl -s "{{ api_base }}/v1/drugs/classes/drugs?class=HMG-CoA%20Reductase%20Inhibitor" -H "X-API-Key: $DRUG_API_KEY"
```

## Example response

`/v1/drugs/class?name=simvastatin` (shape from the OpenAPI schema):

```json
{
  "query_name": "simvastatin",
  "generic_name": "SIMVASTATIN",
  "brand_names": ["Zocor"],
  "classes": [ { "name": "HMG-CoA Reductase Inhibitor", "type": "EPC" } ]
}
```

`/v1/drugs/classes?limit=3` (captured 2026-10-30):

```json
{
  "data": [
    { "name": "4-Hydroxyphenyl-Pyruvate Dioxygenase Inhibitor", "type": "epc" },
    { "name": "5-alpha Reductase Inhibitor", "type": "epc" }
  ],
  "pagination": { "page": 1, "limit": 3, "total": 651, "total_pages": 217 }
}
```

`/v1/drugs/classes/drugs` returns `data` entries of
`{ "generic_name": "ATORVASTATIN CALCIUM", "brand_name": "Lipitor" }` with the same `pagination` block.

## Parameters

| Endpoint | Name | Required | Notes |
|---|---|---|---|
| `/class` | `name` | yes | Generic or brand; brand names fall back to their generic |
| `/classes` | `type` | no | `epc`, `moa`, `pe`, `cs` (see [Glossary](../reference/glossary.md#drug-class-types)) |
| `/classes` | `page`, `limit` | no | Pagination |
| `/classes/drugs` | `class` | yes | Exact class name, URL-encoded |
| `/classes/drugs` | `page`, `limit` | no | Default limit 100, max 500 |

## Errors

| Status | `error` | Meaning |
|---|---|---|
| 400 | `bad_request` | Missing `name`/`class`, or a bad `type` |
| 404 | `not_found` | No drug or class by that name |
| 401 | `unauthorized` | Missing or invalid API key |
| 502 | `upstream_error` | A data source was unreachable; retry |

## Related

- Find the exact class name first with `/v1/drugs/classes`.
- [Glossary: drug class types](../reference/glossary.md#drug-class-types).
