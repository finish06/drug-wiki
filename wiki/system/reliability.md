# Reliability

The government sources behind the API are slow, rate-limited, and sometimes
down. The stack is built so that you mostly don't notice. Here is what each
layer does when something goes wrong.

## When a source is slow or throttling (`429`)

- **cash-drugs paces its big refreshes** (one page at a time, 250 ms apart) to
  stay under DailyMed's limits.
- **Scheduled refreshes retry** a throttled page up to 5 times with backoff,
  honoring the source's `Retry-After`. If a page still fails, the whole refresh
  is discarded and the previous complete list stays.
- **Your requests don't wait on retries:** on-demand lookups fail fast, and
  drug-gate returns `502` so your app can retry later.

## When a source is down

1. **cash-drugs serves its last copy** of whatever it has, marked stale, while it
   keeps trying in the background.
2. **Scheduled lists are never deleted.** The last good copy of the drug-name and
   class lists is kept until a newer complete one replaces it, however long the
   outage lasts.
3. **Circuit breakers** in cash-drugs (per source) and drug-gate (toward cash-drugs)
   stop calling a failing dependency for a cool-down, so requests fail fast instead
   of queuing.
4. **Only if nobody has a copy** do you get `502 upstream_error`. drug-gate's own
   cache also keeps answering for anything it already holds.

## When a load goes wrong

rx-dag only swaps in a new night's NDC data after it loaded completely and its
row counts look sane (no table shrank by more than 20%). Otherwise yesterday's
data stays. See [rx-dag](rx-dag.md).

## Watching it

- Each service exports Prometheus metrics: request rates and latency, cache
  hits, upstream errors, circuit-breaker state.
- **Alerts** fire when a scheduled list hasn't refreshed for twice its schedule,
  when its freshness metric disappears, and when upstream error rates climb.

## What this means for your app

- Retry `502` with backoff; it's usually brief.
- Treat empty results as "no data", not as an error.
- Cache on your side too; the data changes slowly ([Data freshness](data-freshness.md)).
