# PRD: drug-wiki

**Version:** 0.1.0 · **Created:** 2026-10-30 · **Owner:** Caleb Dunn · **Maturity:** alpha

## 1. Problem Statement

The drug-data stack (drug-gate, cash-drugs, ndc-loader) has grown to 15+ public
endpoints, an API-key system and four upstream data sources, but its only
documentation is per-repo READMEs and a Swagger page. Even its owner says:
"this is overwhelming. I do not know what is available, where to start." A
developer who wants to use the API has no single place that answers: how do I
connect, how do I get a key, what can I ask for, and which endpoint fits my use
case?

## 2. Users

- **Caleb** — owner, returning to the stack after time away.
- **Developers building on drug-gate** — a frontend or service that needs drug
  data; never seen the stack, has no key yet.

## 3. Success Metrics

- A new developer makes a first successful authenticated request in under 5
  minutes from the landing page.
- Every public drug-gate `/v1` endpoint appears in the catalog with its use case
  (enforced by a test against drug-gate's OpenAPI).
- Zero broken internal links (strict build in CI).

## 4. Scope

**In:** public developer docs for drug-gate — start here, quickstart, API keys,
use-case guides, endpoint catalog, errors and limits, glossary, interactive
OpenAPI reference, FAQ. Hosted at `https://wiki.drugs.calebdunn.tech`.

**Out (for now):** internal operations (cash-drugs internals, runbooks, hosts,
deploys, alerts) — private, stays in the service repos; self-serve key signup
(a product change in drug-gate).

## 5. Technical Constraints

- Docs-as-code: Markdown in git, MkDocs Material, PR-reviewed, built with
  `--strict`.
- Static site in an nginx container, published to `dockerhub.calebdunn.tech`,
  run on the homelab K3s by the operator (`joe_tmux_1`); public route via the
  VPS edge like other `calebdunn.tech` sites.
- The API base URL is one variable (`extra.api_base` in `mkdocs.yml`).
- The interactive reference is drug-gate's own OpenAPI document, vendored by a
  sync script — no hand-copied schemas.

## 6. Environment Strategy

Tier 2: local (`mkdocs serve`) → production. CI builds and publishes
`:<sha>` images on push to `main`; production moves only when the operator
repoints the Deployment, on Caleb's go.

## 7. Roadmap

- **Now — M1 Wiki v1:** the pages above, CI, hosting.
- **Next:** self-serve key requests; per-endpoint pages generated from OpenAPI;
  versioned docs per drug-gate release.
- **Later:** private ops section behind SSO.
