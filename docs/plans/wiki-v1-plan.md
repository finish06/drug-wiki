# Implementation Plan: Wiki v1

**Spec Version:** 0.1.0 · **Created:** 2026-10-30 · **Team:** Solo (agent) · **Estimate:** ~half a day

## Tasks

| Task | AC | Description | Files |
|------|----|-------------|-------|
| TASK-001 | AC-004, AC-008 | `scripts/sync-openapi.sh` vendors drug-gate's OpenAPI | scripts/, wiki/reference/openapi.json |
| TASK-002 | all | RED: `tests/test_wiki.py` — required pages + nav, catalog covers every `/v1` path, guide template sections, glossary terms, no private details, strict build | tests/ |
| TASK-003 | AC-009 | `mkdocs.yml`: Material, tabs, search, edit links, macros (`api_base`), swagger-ui-tag, git-less last-updated via page meta | mkdocs.yml |
| TASK-004 | AC-001–AC-003 | Start here, Quickstart, API keys, Concepts | wiki/index.md, wiki/get-started/ |
| TASK-005 | AC-005 | Seven guides; examples captured from a real local stack where possible, OpenAPI shapes otherwise (marked) | wiki/guides/ |
| TASK-006 | AC-004, AC-006–AC-008 | Catalog, errors & limits, glossary, Swagger page | wiki/reference/ |
| TASK-007 | AC-012 | FAQ / troubleshooting; how to contribute | wiki/help/ |
| TASK-008 | AC-011 | Dockerfile (build → nginx), nginx.conf, Gitea workflows | Dockerfile, nginx.conf, .gitea/workflows/ |
| TASK-009 | AC-011 | Repo on Gitea, PR, image, operator hosting | — |

## Test Strategy

`pytest` structural tests + `mkdocs build --strict` in CI. Examples come from
real responses captured against a local drug-gate + cash-drugs on 2026-10-30;
endpoints that need ndc-loader or the full drug-name list use OpenAPI shapes.

## Risks

| Risk | Mitigation |
|------|-----------|
| Docs drift from drug-gate | OpenAPI vendored by script; catalog test fails on new paths |
| Public site leaks internals | AC-010 test; ops pages excluded |
| Prod base URL unknown at writing time | Single `api_base` variable, set once the operator confirms |
