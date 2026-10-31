# Implementation Plan: Build the Wiki with Zensical

**Spec Version:** 0.1.0 · **Created:** 2026-10-30 · **Estimate:** ~1h

| Task | AC | Description | Files |
|------|----|-------------|-------|
| TASK-001 | all | RED: tests build with `zensical`, require vendored Swagger UI + init, "Made with Zensical" footer, requirements pins | tests/test_wiki.py |
| TASK-002 | AC-003 | `scripts/vendor-swagger-ui.sh` downloads swagger-ui-dist, checks its sha1 against npm, copies bundle/css/LICENSE to `wiki/assets/swagger-ui/` | scripts/, wiki/assets/ |
| TASK-003 | AC-003 | `wiki/assets/javascripts/swagger-init.js`; `api.md` uses `<div id="swagger-ui" data-spec="…">` | wiki/ |
| TASK-004 | AC-001, AC-005 | requirements, `mkdocs.yml` (drop swagger-ui-tag, add extra_javascript/css) | requirements.txt, mkdocs.yml |
| TASK-005 | AC-006 | Dockerfile, README, CLAUDE.md, contributing page | — |
| TASK-006 | TC-002 | Browser check of the API page; image; operator roll | — |

Risk: Zensical is pre-1.0 → pin exactly; the strict build + tests catch regressions.
