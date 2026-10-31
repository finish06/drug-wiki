# Improve this wiki

This wiki is plain Markdown in git, built with [Zensical](https://zensical.org). Every page has an **edit** (pencil) button
at the top that opens it in the repository.

## Conventions

- **One page, one job.** Guides answer "how do I …"; reference pages answer
  "what exactly is …". Link between them instead of repeating content.
- **Guides use one template:** When to use → Request → Example response →
  Parameters → Errors → Related.
- **Real examples.** Paste responses captured from the API, shortened with `…`.
  Say when an example only shows the schema's shape.
- **Never paste a real API key** or anything private (internal hostnames, IPs, secrets).
  A test rejects common patterns.
- **The base URL lives in one place**: `extra.api_base` in `mkdocs.yml` (Zensical reads it). Write
  `{{ "{{ api_base }}" }}` in pages.

## When the API changes

1. In a drug-gate checkout next to this repo, run `scripts/sync-openapi.sh`.
2. Run `pytest -q`. It fails if a new `/v1` endpoint has no row in
   [All endpoints](../reference/endpoints.md).
3. Add the row (and a guide section if it's a new use case), then open a PR.

## Run it locally

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
zensical serve      # http://127.0.0.1:8000
pytest -q           # structure checks + strict Zensical build
```
