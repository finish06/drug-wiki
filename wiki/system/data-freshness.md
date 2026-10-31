# Data freshness

Data passes through up to three layers: the source, cash-drugs (and rx-dag for
NDCs), then drug-gate's cache. This page says how old each kind of data can be
when it reaches you.

| Data | Source | How it's refreshed | Typical worst-case age |
|---|---|---|---|
| **Drug names** (autocomplete, names list) | FDA DailyMed | Full list re-fetched every 6 hours | ~7 hours |
| **Drug classes** | FDA DailyMed | Full list re-fetched every 6 hours | ~7 hours |
| **NDC products and packages** | FDA NDC Directory, via rx-dag | rx-dag reloads nightly at 03:00; cash-drugs keeps answers 1 hour | ~1 day after the FDA publishes |
| **Product labels (SPL)** and label sections | FDA DailyMed | Fetched on first request; kept up to 48 hours after their last refresh | ~2 days |
| **Drug info / interaction results** | Built from labels | Rebuilt when drug-gate's cached copy expires | Same as labels |
| **RxNorm** IDs, NDCs, generics, related | NLM RxNorm | Fetched on first request; kept 7–30 days | Up to ~30 days |
| **Recalls** (enforcement reports) | openFDA | Refreshed daily at 03:00 | ~1 day (internal only, not yet in the public API) |
| **Shortages** | openFDA | Refreshed daily at 03:00 | ~1 day (internal only, not yet in the public API) |

Notes:

- **Popular items can stay in drug-gate's cache longer.** Each hit extends its
  one-hour cache life, so an item requested constantly keeps its cached copy until
  traffic pauses.
- **During a source outage** the last good copy keeps being served, so data can
  be older than the table says. See [Reliability](reliability.md).
- **Labels change rarely**: a few hundred of the roughly 150,000 change on a typical day.
