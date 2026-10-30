# Spec: Wiki v1 — Developer Docs for drug-gate

**Version:** 0.1.0
**Created:** 2026-10-30
**PRD Reference:** docs/prd.md
**Status:** Draft

## 1. Overview

A public docs site, organized the usual way for developer docs: start-here and quickstart pages (tutorials), use-case guides (how-to), the catalog, errors and OpenAPI pages (reference), and a concepts page (explanation). It answers, in order: what this is and where to start, how to connect, how to get a key,
what APIs exist, and which one fits each use case.

Interview decisions (Caleb, 2026-10-30): public API docs with ops kept private;
audience is Caleb plus developers new to the stack; docs-as-code with MkDocs
Material; host at `wiki.drugs.calebdunn.tech` (Caleb's suggestion).

### User Story

As a **developer who has never used the drug stack**, I want one site that
tells me where to start, how to connect, how to get a key and which endpoint
solves my problem, so that I can make useful requests without reading source.

## 2. Acceptance Criteria

| ID | Criterion | Priority |
|----|-----------|----------|
| AC-001 | **Start here** (`index.md`): what the API is in 2–3 sentences, who it's for, a 3-step path (key → first call → pick a guide), and an "I want to…" table linking every guide | Must |
| AC-002 | **Quickstart**: base URL, the `X-API-Key` header, one copy-paste request in curl, JavaScript and Python, the expected response, and what to read next | Must |
| AC-003 | **API keys**: how to request a key, what you receive (key, rate limit, allowed origins), browser vs server use (origins/CORS), keeping it secret, rotation and lost keys; an admin section showing how a key is issued | Must |
| AC-004 | **Endpoint catalog**: every `/v1` path in drug-gate's OpenAPI document listed with method, one-line purpose and a link to its guide — enforced by a test against the vendored OpenAPI | Must |
| AC-005 | **Use-case guides**, one per task (NDC lookup, search box/autocomplete, drug info card, interaction check, browse by class, RxNorm normalization, product labels). Each has: When to use, Request, Example response, Parameters, Errors, Related | Must |
| AC-006 | **Errors & limits**: error body shape, each status code and what to do, rate-limit headers and 429 handling, and what 502 means | Must |
| AC-007 | **Glossary** of NDC, RxCUI, SPL, set ID, drug class types (EPC, MoA, PE, CS), generic vs brand | Must |
| AC-008 | **Interactive reference**: Swagger UI on drug-gate's OpenAPI, vendored by `scripts/sync-openapi.sh` | Must |
| AC-009 | Wiki practices: full-text search, tabbed navigation, "edit this page" links to the repo, last-updated dates, one `api_base` variable, strict build (no broken links) | Must |
| AC-010 | No private operational detail: no LAN IPs, cluster DNS names, connection strings, admin secrets or cash-drugs internals — enforced by a test | Must |
| AC-011 | Served from a container image (nginx) built in CI; production at `https://wiki.drugs.calebdunn.tech` (operator) | Must |
| AC-012 | **FAQ / troubleshooting** for the common failures (401, 403 origin, 429, 502, empty results, NDC formats) | Should |

## 3. User Test Cases

No UI interactions beyond reading; screenshot checkpoints are the rendered pages.

### TC-001: New developer to first call
**Precondition:** A developer with no key lands on the site.
**Steps:** Read Start here → API keys → Quickstart; run the curl example with a key.
**Expected Result:** 200 with drug data; the page told them which guide to read next.
**Screenshot Checkpoint:** Start here, Quickstart.
**Maps to:** TBD

### TC-002: Find the endpoint for a task
**Precondition:** Developer has a key and a drug's NDC from a bottle.
**Steps:** From Start here's "I want to…" table, open "Look up a drug by NDC".
**Expected Result:** Request, example response, parameters and errors on one page.
**Screenshot Checkpoint:** the guide.
**Maps to:** TBD

### TC-003: Catalog completeness
**Precondition:** Vendored drug-gate OpenAPI.
**Steps:** Run the test suite.
**Expected Result:** Every `/v1` path is in the catalog with a guide link.
**Screenshot Checkpoint:** N/A
**Maps to:** TBD

### TC-004: Live site
**Precondition:** Image deployed by the operator.
**Steps:** Open `https://wiki.drugs.calebdunn.tech`, search "interaction".
**Expected Result:** HTTPS 200, search returns the interaction guide.
**Screenshot Checkpoint:** search results.
**Maps to:** operator verification

## 4. Data Model

Markdown pages under `wiki/`; `wiki/reference/openapi.json` vendored from
drug-gate `docs/swagger.json`.

## 5. API Contract

N/A — static site. Documents drug-gate's API; changes none.

## 6. UI Behavior

MkDocs Material: light/dark toggle, tabs (Get started · Guides · Reference ·
Help), search, copy buttons on code blocks.

## 7. Edge Cases

| Case | Expected Behavior |
|------|------------------|
| drug-gate adds an endpoint | `sync-openapi.sh` + test fails until the catalog lists it |
| Base URL changes | One edit to `extra.api_base` |
| Endpoint broken in prod (e.g. RxNorm 502 before drug-gate #41) | Guide documents the intended behavior; FAQ explains 502 |

## 8. Dependencies

- drug-gate OpenAPI (`docs/swagger.json`, v0.10.0)
- Operator: Deployment, route and DNS for `wiki.drugs.calebdunn.tech`
- Caleb: the key-request channel (default: GitHub issue on finish06/drug-gate)

## 9. Infrastructure Prerequisites

| Category | Requirement |
|----------|-------------|
| Environment variables | None |
| Registry images | `dockerhub.calebdunn.tech/finish06/drug-wiki:<sha>` (CI) |
| Network reachability | Public route + TLS on the VPS edge; DNS for `wiki.drugs.calebdunn.tech` |
| CI status | Gitea Actions (ci-shared@v3) green |
| External secrets | Registry credentials in the new repo's CI secrets |
| Database migrations | None |

**Verified before implementation:** No — operator confirms hosting.

## 10. Revision History

| Date | Version | Author | Changes |
|------|---------|--------|---------|
| 2026-10-30 | 0.1.0 | calebdunn | Initial spec from the /goal request and the 3-question interview |
