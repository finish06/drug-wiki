# Spec: System Section — How the Backend Works

**Version:** 0.1.0
**Created:** 2026-10-30
**PRD Reference:** docs/prd.md
**Status:** In Progress

## 1. Overview

Caleb: "wiki.drugs needs to include explanation of the backend and whole system
too. rx-dag, cash drug and drug gate". A new **System** tab explains the three
services: what each does, how a request flows through them, where data comes
from and how fresh it is, and how the stack stays up when sources fail.

This narrows the PRD's "ops private" boundary: **architecture is public**
(services, responsibilities, data flow, freshness, resilience, public source
repos); **operations stay private** (hostnames, IPs, ports, cluster names,
credentials, runbooks, deploy steps). The AC-010 privacy test keeps enforcing it.

### User Story

As **Caleb or a developer using the API**, I want to understand what runs
behind drug-gate, so that I know where data comes from, why something is slow
or stale, and which service to look at.

## 2. Acceptance Criteria

| ID | Criterion | Priority |
|----|-----------|----------|
| AC-001 | `system/index.md`: the whole system on one page: a diagram of drug-gate → cash-drugs → sources (DailyMed, openFDA, RxNorm, rx-dag → FDA bulk files), one paragraph per service, a request walk-through, and links to each service page | Must |
| AC-002 | One page per service (`drug-gate.md`, `cash-drugs.md`, `rx-dag.md`) with sections in order: What it does → How it works → Data → Interfaces → Reliability → Source code | Must |
| AC-003 | `system/data-freshness.md`: for each kind of data, its source, how it is refreshed and how stale it can be | Must |
| AC-004 | `system/reliability.md`: what happens when a source is slow, throttles or is down, at each layer (stale serving, circuit breakers, pacing/retries, retained last-good copies, monitoring) | Must |
| AC-005 | Each service page links its public source repo on GitHub | Must |
| AC-006 | Start here and How it works link to the System section; System is a nav tab | Must |
| AC-007 | No operational detail (existing AC-010 test) — also no ports | Must |

## 3. User Test Cases

### TC-001: "Why is this data stale?"
**Steps:** From Start here → System → Data freshness.
**Expected Result:** The row for that data says how often it refreshes and the worst-case age.
**Maps to:** tests/test_wiki.py → test_system_ac003_freshness_covers_each_data_kind

### TC-002: "What is rx-dag?"
**Steps:** System → rx-dag.
**Expected Result:** What it loads, when, how cash-drugs uses it, link to source.
**Maps to:** tests/test_wiki.py → test_system_ac002_ac005_service_pages_follow_template_and_link_source[system/rx-dag.md]

## 7. Edge Cases

| Case | Expected Behavior |
|------|------------------|
| A service changes behavior | Pages cite the source repo; update with the change (contributing page) |

## 10. Revision History

| Date | Version | Author | Changes |
|------|---------|--------|---------|
| 2026-10-30 | 0.1.0 | calebdunn | Initial spec from Caleb's request |
| 2026-10-30 | 0.1.0 | calebdunn | Code complete: 8 RED → 30 GREEN. Facts checked against the repos; removed a drug-gate "stale fallback" claim (code exists, nothing calls it) |
