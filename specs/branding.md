# Spec: Pill Branding

**Version:** 0.1.0
**Created:** 2026-10-30
**PRD Reference:** docs/prd.md
**Status:** In Progress

## 1. Overview

Caleb: "set up all three": the three places asyncer.tiangolo.com shows its icon:
the header logo, the favicon and a logo banner at the top of the home page.
The wiki still shows Zensical's default book icon in the header and favicon,
which says "docs" but not "drugs". A pill mark in the site's teal replaces it.

### User Story

As a **developer landing on the wiki**, I want a drug-specific mark in the
header, browser tab and home page, so that I can tell at a glance this is the
drug API's docs and find its tab again.

## 2. Acceptance Criteria

| ID | Criterion | Priority |
|----|-----------|----------|
| AC-001 | Header logo: `theme.logo` is `assets/images/icon.svg`, a single-color teal (#009688) pill SVG. Zensical's modern header follows the page scheme (near-white in light, near-black in dark), so a white mark would vanish in light mode | Must |
| AC-002 | Favicon: `theme.favicon` is `assets/images/favicon.png`, the white pill on a teal tile; the built pages link it instead of the default | Must |
| AC-003 | Home banner: Start here opens with `assets/images/logo.svg` (pill + "Drug API Wiki" wordmark, text as paths so it renders the same everywhere), centered; the page's H1 stays for screen readers and search but is visually hidden | Must |
| AC-004 | The banner is readable on both the light (`default`) and dark (`slate`) schemes: one teal (#009688) that clears 3:1 on both | Should |
| AC-005 | All existing wiki checks still pass under `zensical build --strict` | Must |

## 3. User Test Cases

### TC-001: Header and tab
**Steps:** `zensical serve`; open any page in light then dark mode.
**Expected Result:** Teal pill top-left of the header in both schemes; the browser tab shows the teal pill tile.
**Maps to:** test_branding_ac001_header_logo, test_branding_ac002_favicon

### TC-002: Home banner
**Steps:** Open Start here in light then dark mode.
**Expected Result:** Centered pill + "Drug API Wiki" logo above the intro; no duplicate visible heading.
**Maps to:** test_branding_ac003_home_banner

## 7. Edge Cases

| Case | Expected Behavior |
|------|------------------|
| SVG shown via `<img>` cannot load the page's Inter webfont | Wordmark ships as paths, not `<text>` |
| Mobile nav drawer | Material reuses `theme.logo` there; same teal pill |

## 10. Revision History

| Date | Version | Author | Changes |
|------|---------|--------|---------|
| 2026-10-30 | 0.1.0 | calebdunn | Initial spec from Caleb's request, modelled on asyncer.tiangolo.com |
| 2026-10-30 | 0.1.0 | calebdunn | Code complete: 3 RED → 33 GREEN. Headless Chrome checked header, banner and favicon in light and dark. Header mark changed white → teal after the light-mode check showed the modern theme's header isn't teal |
