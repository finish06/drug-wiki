# All endpoints

Base URL `{{ api_base }}`. Every `/v1` endpoint needs `X-API-Key`. This table
is checked against the API's OpenAPI document on every build, so a new endpoint
can't ship without a row here.

## Drug data (`/v1`)

| Method | Path | Use it to… | Guide |
|---|---|---|---|
| GET | `/v1/drugs/ndc/{ndc}` | Identify a product from its NDC: name, generic name, classes | [NDC lookup](../guides/ndc-lookup.md) |
| GET | `/v1/drugs/autocomplete` | Suggest names as the user types (`q`, 2+ chars) | [Search box](../guides/search-box.md) |
| GET | `/v1/drugs/names` | List or filter all drug names, paginated | [Search box](../guides/search-box.md) |
| GET | `/v1/drugs/info` | Label safety sections for a drug by name or NDC | [Drug info card](../guides/drug-info.md) |
| POST | `/v1/drugs/interactions` | Cross-check 2–10 drugs' labels for mentions of each other | [Interactions](../guides/interactions.md) |
| GET | `/v1/drugs/class` | Classes and brand names for one drug | [Drug classes](../guides/drug-classes.md) |
| GET | `/v1/drugs/classes` | List drug classes, filterable by type | [Drug classes](../guides/drug-classes.md) |
| GET | `/v1/drugs/classes/drugs` | List the drugs in a class | [Drug classes](../guides/drug-classes.md) |
| GET | `/v1/drugs/rxnorm/search` | Fuzzy-match a name to RxNorm concepts | [RxNorm](../guides/rxnorm.md) |
| GET | `/v1/drugs/rxnorm/profile` | Everything about a drug in one call | [RxNorm](../guides/rxnorm.md) |
| GET | `/v1/drugs/rxnorm/{rxcui}/ndcs` | All NDCs for an RxNorm product | [RxNorm](../guides/rxnorm.md) |
| GET | `/v1/drugs/rxnorm/{rxcui}/generics` | Generic equivalents | [RxNorm](../guides/rxnorm.md) |
| GET | `/v1/drugs/rxnorm/{rxcui}/related` | Ingredients, brands, dose forms, products | [RxNorm](../guides/rxnorm.md) |
| GET | `/v1/drugs/spls` | Search a drug's FDA labels | [Product labels](../guides/product-labels.md) |
| GET | `/v1/drugs/spls/{setid}` | One label with parsed sections | [Product labels](../guides/product-labels.md) |

## Service (no key)

| Method | Path | Use it to… |
|---|---|---|
| GET | `/health` | Check the API is up (status and dependencies) |
| GET | `/version` | See the running build |
| GET | `/openapi.json` | Download the machine-readable API description |
| GET | `/swagger/` | The API's own Swagger UI |

These service paths are reachable from US networks only; `/v1` works worldwide.

## Admin (admin secret)

Key management under `/admin/keys`. See [Get an API key → For admins](../get-started/api-keys.md#for-admins-issuing-a-key).
