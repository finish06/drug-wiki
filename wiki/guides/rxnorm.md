# Normalize names with RxNorm

RxNorm is the US standard vocabulary for clinical drugs. Each concept has an
**RxCUI**. Use these endpoints to turn whatever a user typed into a canonical
ID, then get its NDCs, generic equivalents and related concepts.

## When to use

| Need | Endpoint |
|---|---|
| Messy or misspelled name → best matching RxCUIs | `GET /v1/drugs/rxnorm/search?name=` |
| One call for everything about a drug | `GET /v1/drugs/rxnorm/profile?name=` |
| All NDCs for a drug product | `GET /v1/drugs/rxnorm/{rxcui}/ndcs` |
| Generic equivalent of a branded product | `GET /v1/drugs/rxnorm/{rxcui}/generics` |
| Ingredients, brands, dose forms, products | `GET /v1/drugs/rxnorm/{rxcui}/related` |

## Request

```bash
curl -s "{{ api_base }}/v1/drugs/rxnorm/search?name=lipitor" -H "X-API-Key: $DRUG_API_KEY"
curl -s "{{ api_base }}/v1/drugs/rxnorm/profile?name=atorvastatin" -H "X-API-Key: $DRUG_API_KEY"
curl -s "{{ api_base }}/v1/drugs/rxnorm/617312/ndcs" -H "X-API-Key: $DRUG_API_KEY"
```

## Example response

All captured 2026-10-30 and shortened.

Search returns up to 5 candidates, plus spelling suggestions when nothing matches:

```json
{
  "query": "lipitor",
  "candidates": [
    { "rxcui": "153165", "name": "Lipitor", "score": 14 },
    { "rxcui": "1177401", "name": "Lipitor Pill", "score": 13 }
  ],
  "suggestions": []
}
```

Profile:

```json
{
  "query": "atorvastatin",
  "rxcui": "83367",
  "name": "ATORVASTATIN",
  "brand_names": ["Lipitor", "Atorvaliq"],
  "generic": { "rxcui": "83367", "name": "atorvastatin" },
  "ndcs": [],
  "related": {
    "rxcui": "83367",
    "ingredients": [ { "rxcui": "83367", "name": "atorvastatin" } ],
    "brand_names": [ { "rxcui": "153165", "name": "Lipitor" } ],
    "dose_forms": [ { "rxcui": "317541", "name": "Oral Tablet" } ],
    "clinical_drugs": [ { "rxcui": "617312", "name": "atorvastatin 10 MG Oral Tablet" } ],
    "branded_drugs": [ { "rxcui": "262095", "name": "atorvastatin 80 MG Oral Tablet [Lipitor]" } ]
  }
}
```

NDCs for a specific product (rxcui `617312`, atorvastatin 10 MG Oral Tablet):

```json
{ "rxcui": "617312", "ndcs": ["00093505610", "00093505698", "…326 total"] }
```

Generics: `{ "rxcui": "617312", "generics": [ { "rxcui": "617312", "name": "atorvastatin 10 MG Oral Tablet" } ] }`

!!! info "Ingredient vs product"
    An ingredient-level RxCUI (like `83367`, atorvastatin) has **no NDCs**: only
    specific products do. Use `related.clinical_drugs` or `related.branded_drugs`
    to get product RxCUIs, then ask for their NDCs.

## Parameters

| Endpoint | Name | Required | Notes |
|---|---|---|---|
| `/search`, `/profile` | `name` | yes | Any drug name; fuzzy |
| `/{rxcui}/…` | `rxcui` | yes | Numeric RxCUI (path) |

## Errors

| Status | `error` | Meaning |
|---|---|---|
| 400 | `bad_request` | `name` missing |
| 404 | `not_found` | No match for the name, or unknown RxCUI |
| 401 | `unauthorized` | Missing or invalid API key |
| 502 | `upstream_error` | RxNorm unreachable; retry |

## Related

- NDC → product details: [Look up a drug by NDC](ndc-lookup.md).
- [Glossary: RxCUI](../reference/glossary.md).
