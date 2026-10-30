# drug-wiki

Public developer docs for drug-gate (https://wiki.drugs.calebdunn.tech). Follows ADD: PRD → spec → plan → tests → pages.

- Content in `wiki/` (MkDocs `docs_dir`); ADD docs in `docs/` and `specs/`.
- Public site: never add internal hosts, IPs, cluster DNS, secrets or ops detail (tests/test_wiki.py AC-010). Ops docs stay in the service repos.
- Guides follow: When to use → Request → Example response → Parameters → Errors → Related.
- Examples are real responses (captured) unless marked as schema shape.
- After drug-gate API changes: `scripts/sync-openapi.sh ../drug-gate`, then `pytest -q`.
- Deploy: CI publishes `dockerhub.calebdunn.tech/finish06/drug-wiki:<sha>`; operator `joe_tmux_1` pins prod by digest on Caleb's go.
