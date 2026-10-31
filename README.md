# drug-wiki

Public developer wiki for the drug-gate API, published at
**https://wiki.drugs.calebdunn.tech**. Built with [Zensical](https://zensical.org) (config stays in `mkdocs.yml`), docs-as-code.

- Pages: `wiki/` · Config: `mkdocs.yml` (`extra.api_base` is the one API URL)
- Run locally: `pip install -r requirements.txt && zensical serve`
- Test: `pytest -q` (structure, endpoint coverage vs drug-gate OpenAPI, no private details, strict build)
- Sync the API reference: `scripts/sync-openapi.sh ../drug-gate`; Swagger UI assets: `scripts/vendor-swagger-ui.sh [version]`
- Image: `Dockerfile` builds the site into `nginx-unprivileged` on :8080, health at `/healthz`
- ADD: `docs/prd.md`, `specs/wiki-v1.md`, `docs/plans/wiki-v1-plan.md`
