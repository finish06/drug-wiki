# cash-drugs

## What it does

cash-drugs is the stack's **caching proxy**. Every government API the stack uses
is described once in its configuration as a named endpoint (a *slug*). Internal
services ask cash-drugs for a slug instead of calling the source. cash-drugs:

- fetches from the source **once** and stores the result, so ten callers mean
  one upstream request, not ten;
- **refreshes** the big lists (all drug names, all drug classes, recalls,
  shortages) on a schedule, so they are always ready;
- **paces** itself to stay under each source's rate limit;
- **keeps serving** its last good copy when a source is slow or down.

It's internal: only drug-gate calls it.

## How it works

A Go service backed by MongoDB, with an in-memory cache in front for hot items.
Each slug says where to fetch (base URL, path, query parameters), how to page
through results, how long a copy stays fresh (TTL), and, for the big lists, a
refresh schedule.

When a request comes in for a slug:

1. **Fresh copy stored?** Return it, usually in under 50 ms.
2. **Stale copy stored?** Return it immediately and refresh it in the background
   (stale-while-revalidate).
3. **Nothing stored?** Fetch from the source, store the result, return it.

Scheduled refreshes run on one instance (the **leader**). Other instances only
serve. A per-slug lock makes sure each list is walked by one worker at a time.

## Data

| Group | Slugs | Source |
|---|---|---|
| Drug names, classes | `drugnames`, `drugclasses` | DailyMed (full lists, refreshed every 6 h) |
| Product labels | `spls-by-name`, `spl-latest-by-name`, `spl-detail`, `spl-xml`, `spls-by-class` | DailyMed (on demand) |
| NDC products | `fda-ndc`, `rx-dag-ndc-search`, `rx-dag-ndc-lookup`, `rx-dag-ndc-packages` | [rx-dag](rx-dag.md) |
| FDA label text, recalls, shortages | `fda-label`, `fda-enforcement`, `fda-shortages` | openFDA (recalls and shortages refreshed daily) |
| RxNorm | `rxnorm-*` (search, spelling, NDCs, generics, related) | NLM RxNorm (on demand, kept for days) |

Every stored copy records where it came from and when it was fetched. Copies of
scheduled lists are kept indefinitely as the "last good copy"; on-demand copies
are removed 48 hours after their last refresh.

## Interfaces

- **Data:** `/api/cache/{slug}` with the slug's parameters. The response is the data plus metadata: source, `fetched_at`, page count and a `stale` flag.
- **Discovery and tools:** list of configured endpoints, cross-slug search, autocomplete, cache status, warm-up, config validation and a dry-run test fetch.
- **Operations:** `/health`, `/ready` (false until warm-up finishes), `/version`, Prometheus `/metrics`.
- **Errors:** stable codes such as `CD-U001` (source failed, nothing cached) and `CD-U003` (circuit breaker open).

## Reliability

- **Stale beats nothing:** an expired copy is served while a refresh runs. If the
  source is down, the last copy is served with `stale: true`.
- **Pacing and retries for big lists:** full DailyMed walks fetch one page at a
  time, 250 ms apart. A `429`/`503` is retried up to 5 times with backoff,
  honoring `Retry-After`. A walk with any failed page is discarded, so the
  previous complete copy stays.
- **On-demand lookups fail fast:** a user's request never waits through retry backoff.
- **Circuit breaker per source:** a failing source is skipped for a cool-down
  instead of being hammered.
- **Monitoring:** per-slug "last successful refresh" metrics with alerts when a
  list hasn't refreshed for twice its schedule, plus upstream error-rate alerts.

## Source code

[github.com/finish06/cash-drugs](https://github.com/finish06/cash-drugs): Go, MongoDB, Prometheus.
