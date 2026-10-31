# drug-gate

## What it does

drug-gate is the public API at `{{ api_base }}`. It's the only part of the stack
you talk to. It:

- **authenticates** each request with an API key and enforces the key's
  per-minute **rate limit** and allowed browser **origins**;
- **normalizes input**: NDC formats, drug names, pagination;
- **shapes data**: it turns raw source responses (DailyMed label XML, RxNorm
  concept groups, FDA product records) into the small, consistent JSON in the
  [guides](../guides/ndc-lookup.md);
- **combines sources** for higher-level features: the [drug info card](../guides/drug-info.md),
  the [interaction checker](../guides/interactions.md) and the [RxNorm profile](../guides/rxnorm.md).

## How it works

A Go service with a Redis store. Every `/v1` request passes through, in order:
request ID → logging and metrics → API key check → per-key rate limit → CORS →
the handler.

Handlers call internal clients that talk only to [cash-drugs](cash-drugs.md),
never to government APIs directly. Results are cached in Redis:

| Data | Cached for |
|---|---|
| Names, classes, NDC lookups, labels, drug info | 60 minutes, extended on every hit |
| RxNorm search and profile | 24 hours |
| RxNorm IDs, NDCs, generics, related | 7 days |

Two background jobs keep common things fast:

- **Autocomplete index:** the full list of ~104,000 drug names is held in memory
  as a sorted index, so prefix suggestions take a few milliseconds.
- **Interaction indexer:** once a day it pre-builds drug info for up to 200 drug
  names that aren't cached yet.

## Data

drug-gate owns only:

- **API keys**: app name, allowed origins, rate limit, active flag, rotation
  grace period;
- **rate-limit counters**: a sliding one-minute window per key;
- **its response cache**.

All drug data comes from cash-drugs.

## Interfaces

- **Public:** the `/v1` drug endpoints ([All endpoints](../reference/endpoints.md)), plus `/health`, `/version`, `/openapi.json` and `/swagger/`.
- **Admin:** `/admin/keys` for issuing, listing, rotating and deactivating keys, protected by an admin secret ([Get an API key](../get-started/api-keys.md#for-admins-issuing-a-key)).
- **Upstream:** cash-drugs' cache endpoints for each data source.
- **Metrics:** Prometheus metrics for request counts and latency per route, cache hits and misses, auth and rate-limit rejections, and Redis health.

## Reliability

- **Circuit breaker** on calls to cash-drugs: after 10 consecutive failures it
  stops calling for 30 seconds and fails fast instead of piling up slow requests.
- **Request coalescing:** many simultaneous requests for the same uncached item
  produce one upstream call; the rest wait for its answer.
- **Loud failure over wrong answers:** if an upstream lookup it depends on is
  missing, drug-gate returns `502` rather than an empty "no results".

See [Reliability](reliability.md) for the whole stack.

## Source code

[github.com/finish06/drug-gate](https://github.com/finish06/drug-gate): Go, chi, Redis.
