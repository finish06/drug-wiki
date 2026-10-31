# drug-wiki

Public developer docs for drug-gate (https://wiki.drugs.calebdunn.tech). Follows ADD: PRD → spec → plan → tests → pages.

- Built with Zensical (`zensical build --strict`), config in `mkdocs.yml`. Zensical silently ignores unsupported MkDocs plugins: check https://zensical.org/docs/compatibility/mkdocs/plugins/ before adding one.
- Content in `wiki/` (`docs_dir`); ADD docs in `docs/` and `specs/`. Swagger UI is vendored in `wiki/assets/swagger-ui/`.
- Public site: never add internal hosts, IPs, cluster DNS, secrets or ops detail (tests/test_wiki.py AC-010). Ops docs stay in the service repos.
- Guides follow: When to use → Request → Example response → Parameters → Errors → Related.
- Examples are real responses (captured) unless marked as schema shape.
- After drug-gate API changes: `scripts/sync-openapi.sh ../drug-gate`, then `pytest -q`.
- Deploy: **every merge to `main` deploys to prod** (`.gitea/workflows/staging-release.yml` applies `k8s/overlays/prod` with the new tag, waits for the rollout, rolls back on failure, smoke-tests `/healthz`). Credential: repo secret `WIKI_KUBECONFIG` for SA `drug-wiki-deployer` (`k8s/deployer-rbac.yaml`, applied by the operator only). Rollback: revert the PR. If the pipeline auto-rolled back (or you ran `kubectl -n drugs rollout undo deploy/drug-wiki`), still revert the PR so `main` matches prod.
- `k8s/` is public (GitHub mirror): never add private hosts/IPs; the LAN Traefik route lives in homelab.
