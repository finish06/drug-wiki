# drug-wiki

Public developer docs for drug-gate (https://wiki.drugs.calebdunn.tech). Follows ADD: PRD → spec → plan → tests → pages.

- Built with Zensical (`zensical build --strict`), config in `mkdocs.yml`. Zensical silently ignores unsupported MkDocs plugins: check https://zensical.org/docs/compatibility/mkdocs/plugins/ before adding one.
- Content in `wiki/` (`docs_dir`); ADD docs in `docs/` and `specs/`. Swagger UI is vendored in `wiki/assets/swagger-ui/`.
- Public site: never add internal hosts, IPs, cluster DNS, secrets or ops detail (tests/test_wiki.py AC-010). Ops docs stay in the service repos.
- Guides follow: When to use → Request → Example response → Parameters → Errors → Related.
- Examples are real responses (captured) unless marked as schema shape.
- After drug-gate API changes: `scripts/sync-openapi.sh ../drug-gate`, then `pytest -q`.
- Deploy: CI publishes `dockerhub.calebdunn.tech/finish06/drug-wiki:<sha>`; operator `joe_tmux_1` pins prod by digest on Caleb's go.
