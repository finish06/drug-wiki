# Show a drug info card

Get the key safety sections of a drug's FDA label in one call: **interactions,
contraindications, warnings and adverse reactions**, by drug name or by NDC.

## When to use

- A drug detail screen ("what should I know about warfarin?").
- After an [NDC lookup](ndc-lookup.md) or a [search box](search-box.md) pick.

## Request

```bash
# by name
curl -s "{{ api_base }}/v1/drugs/info?name=warfarin" -H "X-API-Key: $DRUG_API_KEY"

# by NDC (resolved to its generic name first; takes precedence over name)
curl -s "{{ api_base }}/v1/drugs/info?ndc=00069-3150" -H "X-API-Key: $DRUG_API_KEY"
```

## Example response

```json
{
  "drug_name": "warfarin",
  "input_type": "name",
  "input_value": "warfarin",
  "spl": {
    "title": "WARFARIN SODIUM TABLET [SUN PHARMACEUTICAL INDUSTRIES, INC.]",
    "setid": "8ad881e0-ca41-42ad-9d7d-eb85b3a30af0",
    "published_date": "Oct 26, 2026",
    "spl_version": 15
  },
  "interactions": [
    { "title": "7 DRUG INTERACTIONS", "text": "Concomitant use of drugs that increase bleeding risk, antibiotics, antifungals, …" },
    { "title": "7.1 General Information", "text": "Drugs may interact with warfarin sodium through pharmacodynamic or pharmacokinetic mechanisms. …" }
  ],
  "contraindications": [
    { "title": "4 CONTRAINDICATIONS", "text": "Warfarin sodium tablets, USP are contraindicated in: Pregnancy …" }
  ],
  "warnings": [ { "title": "5 WARNINGS AND PRECAUTIONS", "text": "…" } ],
  "adverse_reactions": [ { "title": "6 ADVERSE REACTIONS", "text": "…" } ]
}
```

*Captured from the API on 2026-10-30, text shortened.*

- `spl` is the label the sections came from: the **most recently published**
  label for that name. Link to it, or fetch it again, with its `setid` ([Read product labels](product-labels.md)).
- Each section list can be **empty**. Over-the-counter "Drug Facts" labels don't
  use numbered sections 4–7, so an OTC product often returns empty lists.

## Parameters

| Name | Required | Notes |
|---|---|---|
| `name` | one of | Generic or brand name, case-insensitive |
| `ndc` | one of | Product NDC; wins if both are given |

## Errors

| Status | `error` | Meaning |
|---|---|---|
| 400 | `bad_request` | Neither `name` nor `ndc` given |
| 404 | `not_found` | The NDC didn't resolve to a drug |
| 401 | `unauthorized` | Missing or invalid API key |
| 502 | `upstream_error` | A data source was unreachable; retry |

A name with no label returns `200` with `spl` set to `null` and empty sections.

## Related

- Several drugs at once: [Check drug interactions](interactions.md).
- Full label list for a drug: [Read product labels](product-labels.md).
