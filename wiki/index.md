---
title: Start here
---

<div align="center" markdown>
![](assets/images/logo.svg){ width="320" }
</div>

# Drug API Wiki { .md-visually-hidden }

**drug-gate** is a REST API for drug information. One API key gives you US drug
names, NDC codes, drug classes, FDA product labels, interaction checks and
RxNorm identifiers. It gathers them from FDA DailyMed, openFDA and the National
Library of Medicine's RxNorm, caches them, and returns clean JSON.

It's for developers building an app, a pharmacy tool or a script that needs
drug data, without integrating four government APIs themselves.

!!! tip "New here? Three steps"
    1. **[Get an API key](get-started/api-keys.md)**: every `/v1` request needs one.
    2. **[Make your first request](get-started/quickstart.md)**: one copy-paste command, about 5 minutes.
    3. **Pick the guide for what you're building** from the table below.

## I want to…

| I want to… | Read | Main endpoint |
|---|---|---|
| Identify a drug from the NDC on a package | [Look up a drug by NDC](guides/ndc-lookup.md) | `GET /v1/drugs/ndc/{ndc}` |
| Add a drug search box with suggestions as you type | [Build a drug search box](guides/search-box.md) | `GET /v1/drugs/autocomplete` |
| Show a drug's warnings, contraindications and side effects | [Show a drug info card](guides/drug-info.md) | `GET /v1/drugs/info` |
| Check whether two or more drugs interact | [Check drug interactions](guides/interactions.md) | `POST /v1/drugs/interactions` |
| Find a drug's class, or every drug in a class | [Browse by drug class](guides/drug-classes.md) | `GET /v1/drugs/class` |
| Turn a messy or misspelled name into a standard ID, find generics | [Normalize names with RxNorm](guides/rxnorm.md) | `GET /v1/drugs/rxnorm/search` |
| Find and read a drug's official FDA label | [Read product labels](guides/product-labels.md) | `GET /v1/drugs/spls` |

Want the full list? See **[All endpoints](reference/endpoints.md)** or try them
live in the **[interactive API](reference/api.md)**.

## The essentials

| | |
|---|---|
| **Base URL** | `{{ api_base }}` |
| **Auth** | Header `X-API-Key: <your key>` on every `/v1` request |
| **Format** | JSON in, JSON out |
| **Rate limit** | Per key, requests per minute. See [Errors and rate limits](reference/errors.md) |
| **Errors** | `{"error": "<code>", "message": "<text>"}` with a standard HTTP status |

!!! warning "Not medical advice"
    The data comes from FDA labels and NLM terminologies, and the interaction
    check matches label text. Use it to inform people, not to make clinical
    decisions.

## Where to go next

- Stuck on an error? See [FAQ and troubleshooting](help/faq.md).
- Unfamiliar term (NDC, RxCUI, SPL)? See the [Glossary](reference/glossary.md).
- Curious how the data flows? See [How it works](get-started/concepts.md), then the
  [System](system/index.md) section for the backend: drug-gate, cash-drugs and rx-dag.
