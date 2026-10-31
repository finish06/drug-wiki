# Spec: Build the Wiki with Zensical

**Version:** 0.1.0
**Created:** 2026-10-30
**PRD Reference:** docs/prd.md
**Status:** In Progress

## 1. Overview

Caleb: "We need to migrate mkdocs to Made with Zensical." Zensical is the
successor to MkDocs + Material for MkDocs from the same team (MkDocs 1.x build
output already warns about it). It reads the existing `mkdocs.yml`, supports
`macros` natively, and renders the same Material UI; its footer reads
"Made with Zensical".

Checked on 2026-10-30 with zensical 0.0.74 against the current site:
- `zensical build --strict` builds every page with no issues; `{{ api_base }}`
  renders without `mkdocs-macros-plugin` installed.
- `swagger-ui-tag` is **silently ignored** (unsupported plugins are not run), so
  the interactive API page would ship blank: `<swagger-ui>` is left as raw HTML.
- The search index moves to `/search.json`.

### User Story

As the **wiki maintainer**, I want the site built with Zensical instead of
MkDocs, so that it stays on the supported toolchain, with the same pages and URLs.

## 2. Acceptance Criteria

| ID | Criterion | Priority |
|----|-----------|----------|
| AC-001 | The site builds with `zensical build --strict`; `requirements.txt` pins `zensical` and drops `mkdocs`, `mkdocs-material`, `mkdocs-macros-plugin` and `mkdocs-swagger-ui-tag` | Must |
| AC-002 | Every existing page keeps its URL, and `{{ api_base }}` still renders the production base URL | Must |
| AC-003 | The interactive API page renders Swagger UI from vendored, pinned `swagger-ui-dist` assets (no CDN) via `extra_javascript`/`extra_css` and an init script, loading `openapi.json` | Must |
| AC-004 | The built footer carries "Made with Zensical" | Must |
| AC-005 | `mkdocs.yml` lists no plugin Zensical ignores (`swagger-ui-tag`); config stays in `mkdocs.yml` (supported) | Should |
| AC-006 | Dockerfile, CI, README, CLAUDE.md and the contributing page use `zensical` commands; the container still serves on :8080 with `/healthz` | Must |
| AC-007 | All existing wiki checks (content, catalog vs OpenAPI, privacy, container) still pass | Must |

## 3. User Test Cases

### TC-001: Same site, new engine
**Steps:** `zensical build --strict`; open Start here, Quickstart, a guide.
**Expected Result:** Same content and URLs; footer says "Made with Zensical".
**Maps to:** tests/test_wiki.py → test_ac009_strict_zensical_build_keeps_urls, test_zensical_ac004_footer_made_with_zensical

### TC-002: Interactive API page
**Steps:** Open /reference/api/ in a browser.
**Expected Result:** Swagger UI lists the drug-gate endpoints; Authorize accepts an API key.
**Maps to:** test_zensical_ac003_api_page_loads_swagger_assets + headless Chrome (48 operations, Authorize button)

### TC-003: Live
**Steps:** Operator rolls the new image; open https://wiki.drugs.calebdunn.tech.
**Expected Result:** 200s as before; footer "Made with Zensical"; API page renders.
**Maps to:** operator verification

## 7. Edge Cases

| Case | Expected Behavior |
|------|------------------|
| Zensical adds a plugin we rely on later | Config stays MkDocs-compatible; revisit |
| swagger-ui upgrade | Re-vendor with `scripts/vendor-swagger-ui.sh <version>` (checksum vs npm) |

## 8. Dependencies

- zensical 0.0.74 (pre-1.0: pinned exactly)
- swagger-ui-dist 5.17.14 (npm sha1 e2c222e5bf9e15ccf80ec4bc08b4aaac09792fd6, verified)

## 10. Revision History

| Date | Version | Author | Changes |
|------|---------|--------|---------|
| 2026-10-30 | 0.1.0 | calebdunn | Initial spec from Caleb's request + compatibility spike |
| 2026-10-30 | 0.1.0 | calebdunn | Code complete: 4 RED → 22 GREEN; headless Chrome renders Swagger UI; image smoke /healthz /, /reference/api/, /search.json 200, /nope 404. Operator roll pending |

Test changes: AC-008 and AC-009 of specs/wiki-v1.md asserted the MkDocs-only
`swagger-ui-tag` plugin, the `<swagger-ui>` tag and `mkdocs build`. They are
rewritten here by request (engine change), not to make code pass.
