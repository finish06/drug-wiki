# Check drug interactions

Send 2 to 10 drugs, by name or NDC, and get back every place where one drug's
FDA label mentions another.

## When to use

- A medication list screen ("are these OK together?").
- Screening a new prescription against a patient's current drugs.

!!! warning
    This matches label text. It finds what the labels *say*, not every clinically
    significant interaction. Don't use it as the only check in a clinical setting.

## Request

```bash
curl -s -X POST "{{ api_base }}/v1/drugs/interactions" \
  -H "X-API-Key: $DRUG_API_KEY" -H "Content-Type: application/json" \
  -d '{"drugs": [{"name": "warfarin"}, {"name": "aspirin"}]}'
```

Mix names and NDCs freely: `{"drugs": [{"name": "warfarin"}, {"ndc": "00069-3150"}]}`.

## Example response

```json
{
  "drugs": [
    { "input_name": "warfarin", "input_type": "name", "resolved_name": "warfarin",
      "has_interactions": true, "spl_setid": "8ad881e0-ca41-42ad-9d7d-eb85b3a30af0" },
    { "input_name": "aspirin", "input_type": "name", "resolved_name": "aspirin",
      "has_interactions": false, "spl_setid": "56474a81-6e10-6c67-e063-6294a90a28c5" }
  ],
  "interactions": [
    { "drug_a": "warfarin", "drug_b": "aspirin", "source": "warfarin",
      "section_title": "7.3 Drugs that Increase Bleeding Risk",
      "text": "Examples of drugs known to increase the risk of bleeding are presented in Table 3. …",
      "spl_setid": "8ad881e0-ca41-42ad-9d7d-eb85b3a30af0" }
  ],
  "checked_pairs": 1,
  "found_interactions": 1
}
```

*Captured from the API on 2026-10-30, text shortened.*

How to read it:

- `drugs[]` has one entry per input, in order. If a drug couldn't be resolved it
  carries an `error` message and is skipped; the rest are still checked.
- `has_interactions` means that drug's label *has* an interactions section. It
  doesn't mean it interacts with the others.
- `interactions[]` has one match per (label, other drug): `source` is the drug
  whose label mentions `drug_b`, quoted in `section_title` and `text`.
- `checked_pairs` counts the pairs compared; duplicate drugs are skipped.

## Parameters

Body (JSON):

| Field | Required | Notes |
|---|---|---|
| `drugs` | yes | 2–10 items |
| `drugs[].name` | one of | Generic or brand name |
| `drugs[].ndc` | one of | Product NDC (resolved to its generic name) |

## Errors

| Status | `error` | Meaning |
|---|---|---|
| 400 | `bad_request` | Fewer than 2 or more than 10 drugs, or malformed JSON |
| 401 | `unauthorized` | Missing or invalid API key |
| 502 | `upstream_error` | A data source was unreachable; retry |

Per-drug problems (unknown NDC, source timeout) appear in that drug's `error`
field with a `200` overall.

## Related

- One drug in depth: [Show a drug info card](drug-info.md).
- The label behind a match: [Read product labels](product-labels.md) using `spl_setid`.
