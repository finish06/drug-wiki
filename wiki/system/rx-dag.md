# rx-dag

## What it does

rx-dag (the service is named **ndc-loader**) keeps a complete local copy of the
FDA's drug product databases and serves fast lookups from it:

- the **NDC Directory**: every listed drug product and package, by National Drug Code;
- **Drugs@FDA**: applications, approved products, submissions, marketing status
  and therapeutic-equivalence codes.

It replaced live calls to openFDA's NDC API, which was slow and rate-limited.
Every NDC lookup in the stack is answered from rx-dag's copy.

## How it works

A Go service backed by PostgreSQL. Every night at 03:00 it:

1. **discovers and downloads** the FDA bulk files;
2. **extracts and parses** them;
3. **loads each table** into a staging copy;
4. **checks the row count**: if a table shrank by more than 20% compared with the
   last load, the load is rejected as suspicious;
5. **swaps** the staging copy in atomically, so readers never see a half-loaded table;
6. **records a checkpoint** per table, so an interrupted load can resume.

A load can also be started by an admin request.

## Data

| Table | From | Holds |
|---|---|---|
| `products` | NDC Directory | One row per product NDC: names, labeler, dosage form, route, active ingredients, classes |
| `packages` | NDC Directory | One row per package NDC: package description, marketing dates |
| `applications`, `drugsfda_products` | Drugs@FDA | Approval applications and their products |
| `submissions`, `marketing_status`, `te_codes` | Drugs@FDA | Submission history, marketing status, therapeutic-equivalence codes |

Lookups accept any NDC format (with or without dashes, 10 or 11 digits) and
normalize it.

## Interfaces

All behind an API key, internal only (cash-drugs is the caller):

- **Lookup:** one product by NDC, and its packages.
- **Search:** full-text search across products.
- **openFDA-compatible:** the same request and response shape as openFDA's
  `/drug/ndc.json`, so callers written for openFDA work unchanged. This is what
  drug-gate's [NDC lookup](../guides/ndc-lookup.md) uses through cash-drugs.
- **Stats and admin:** dataset counts, start a load, load status with checkpoints.
- **Operations:** health, version, Prometheus metrics, Swagger UI.

## Reliability

- **Readers always see the last good load:** a new load only replaces a table
  after it fully loaded and passed the row-count check. A failed or suspicious
  night leaves yesterday's data in place.
- **Resumable loads:** per-table checkpoints let an interrupted load continue.
- **Freshness downstream:** cash-drugs keeps rx-dag answers for at most an hour,
  so a nightly reload reaches the public API within about an hour.

## Source code

[github.com/finish06/ndc-loader](https://github.com/finish06/ndc-loader): Go, chi, PostgreSQL.
