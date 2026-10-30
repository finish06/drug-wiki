# drug-wiki

Public developer wiki for the drug-gate API, published at
**https://wiki.drugs.calebdunn.tech**. MkDocs Material, docs-as-code.

- Pages: `wiki/` · Config: `mkdocs.yml` (`extra.api_base` is the one API URL)
- Run locally: `pip install -r requirements.txt && mkdocs serve`
- Test: `pytest -q` (structure, endpoint coverage vs drug-gate OpenAPI, no private details, strict build)
- Sync the API reference: `scripts/sync-openapi.sh ../drug-gate`
- Image: `Dockerfile` builds the site into `nginx-unprivileged` on :8080, health at `/healthz`
- ADD: `docs/prd.md`, `specs/wiki-v1.md`, `docs/plans/wiki-v1-plan.md`
