# Look up a drug by NDC

Turn the **National Drug Code** printed on a package or bottle into the drug's
brand name, generic name and drug classes.

## When to use

- A user scans or types the NDC from a package (pill identifier, pharmacy intake).
- You have NDCs in prescription or claims data and need readable names.

To get *label* information (warnings, interactions) for an NDC, use
[`/v1/drugs/info?ndc=`](drug-info.md) instead. It resolves the NDC to its
generic name for you.

## Request

```bash
curl -s "{{ api_base }}/v1/drugs/ndc/00069-3150" -H "X-API-Key: $DRUG_API_KEY"
```

## Example response

```json
{
  "ndc": "00069-3150",
  "name": "Lipitor",
  "generic_name": "ATORVASTATIN CALCIUM",
  "classes": ["HMG-CoA Reductase Inhibitor"]
}
```

*Shape from the API's OpenAPI schema.*

## Parameters

| Name | In | Required | Notes |
|---|---|---|---|
| `ndc` | path | yes | Product NDC. Dashed forms `5-4`, `4-4` and `5-3` are accepted and normalized, e.g. `00069-3150` or `0069-3150`. A full 11-digit package NDC (with a package segment) identifies one package size; use the product part when in doubt. |

## Errors

| Status | `error` | Meaning |
|---|---|---|
| 400 | `bad_request` | Not a valid NDC format. The message says why |
| 404 | `not_found` | Valid format, but no product has that NDC |
| 401 | `unauthorized` | Missing or invalid API key |
| 502 | `upstream_error` | The NDC data source was unreachable; retry |

## Related

- [Show a drug info card](drug-info.md): label sections by NDC.
- [Normalize names with RxNorm](rxnorm.md): `GET /v1/drugs/rxnorm/{rxcui}/ndcs` goes the other way, listing every NDC for a drug.
- [Glossary: NDC](../reference/glossary.md).
