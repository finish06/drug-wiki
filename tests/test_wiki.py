"""Structural tests for the wiki (specs/wiki-v1.md).

Run from the repo root: pytest -q
"""
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
OPENAPI = WIKI / "reference" / "openapi.json"

GUIDES = [
    "guides/ndc-lookup.md",
    "guides/search-box.md",
    "guides/drug-info.md",
    "guides/interactions.md",
    "guides/drug-classes.md",
    "guides/rxnorm.md",
    "guides/product-labels.md",
]
GUIDE_SECTIONS = ["## When to use", "## Request", "## Example response", "## Parameters", "## Errors", "## Related"]


def read(rel):
    return (WIKI / rel).read_text()


def nav_files(nav):
    for item in nav:
        if isinstance(item, str):
            yield item
        elif isinstance(item, dict):
            for v in item.values():
                yield from nav_files(v if isinstance(v, list) else [v])


def load_config():
    # mkdocs.yml uses !!python/name tags for pymdownx; ignore them for structure checks.
    class Loader(yaml.SafeLoader):
        pass

    Loader.add_multi_constructor("tag:yaml.org,2002:python/", lambda loader, suffix, node: None)
    return yaml.load((ROOT / "mkdocs.yml").read_text(), Loader=Loader)


# AC-001
def test_ac001_start_here_links_every_guide():
    index = read("index.md")
    assert "I want to" in index
    for guide in GUIDES:
        assert guide in index, f"Start here does not link {guide}"
    for step in ("api-keys.md", "quickstart.md"):
        assert step in index


# AC-002
def test_ac002_quickstart_has_base_url_header_and_three_languages():
    qs = read("get-started/quickstart.md")
    assert "{{ api_base }}" in qs
    assert "X-API-Key" in qs
    for lang in ("```bash", "```javascript", "```python"):
        assert lang in qs, f"quickstart lacks a {lang} example"
    assert "## Next" in qs


# AC-003
def test_ac003_api_keys_page_covers_request_use_and_issue():
    keys = read("get-started/api-keys.md").lower()
    for topic in ("request a key", "rate limit", "origins", "rotate", "lost", "/admin/keys"):
        assert topic in keys, f"API keys page does not cover {topic!r}"


# AC-004
def test_ac004_catalog_lists_every_v1_path_with_a_guide_link():
    spec = json.loads(OPENAPI.read_text())
    catalog = read("reference/endpoints.md")
    paths = [p for p in spec["paths"] if p.startswith("/v1/")]
    assert paths, "vendored OpenAPI has no /v1 paths"
    for path in paths:
        rows = [line for line in catalog.splitlines() if f"`{path}`" in line]
        assert rows, f"catalog is missing {path}"
        assert any("../guides/" in r for r in rows), f"catalog row for {path} has no guide link"


# AC-005
@pytest.mark.parametrize("guide", GUIDES)
def test_ac005_guides_follow_the_template(guide):
    text = read(guide)
    positions = [text.find(s) for s in GUIDE_SECTIONS]
    assert all(p >= 0 for p in positions), f"{guide} lacks {[s for s, p in zip(GUIDE_SECTIONS, positions) if p < 0]}"
    assert positions == sorted(positions), f"{guide} sections out of order"


# AC-006
def test_ac006_errors_page_covers_statuses_and_rate_limit_headers():
    errors = read("reference/errors.md")
    for item in ("400", "401", "403", "404", "429", "502", "X-RateLimit-Remaining", "Retry-After", '"error"'):
        assert item in errors, f"errors page does not cover {item}"


# AC-007
def test_ac007_glossary_terms():
    glossary = read("reference/glossary.md")
    for term in ("NDC", "RxCUI", "SPL", "Set ID", "EPC", "MoA", "Generic", "Brand"):
        assert f"**{term}" in glossary, f"glossary lacks {term}"


# AC-008
def test_ac008_interactive_reference_embeds_vendored_openapi():
    assert "<swagger-ui" in read("reference/api.md") and "openapi.json" in read("reference/api.md")
    assert json.loads(OPENAPI.read_text())["host"] == "drug-gate.calebdunn.tech"


# AC-009
def test_ac009_config_wiki_practices():
    cfg = load_config()
    features = cfg["theme"]["features"]
    for feature in ("navigation.tabs", "search.suggest", "content.action.edit", "content.code.copy"):
        assert feature in features
    plugin_names = [p if isinstance(p, str) else next(iter(p)) for p in cfg["plugins"]]
    for plugin in ("search", "macros", "swagger-ui-tag"):
        assert plugin in plugin_names
    assert cfg["extra"]["api_base"] == "https://drug-gate.calebdunn.tech"
    assert cfg.get("edit_uri") and cfg.get("repo_url")
    for rel in nav_files(cfg["nav"]):
        assert (WIKI / rel).exists(), f"nav points at missing {rel}"
    for page in WIKI.rglob("*.md"):
        assert str(page.relative_to(WIKI)) in set(nav_files(cfg["nav"])), f"{page} is not in nav"


# AC-010
PRIVATE = [
    r"192\.168\.", r"\b10\.17\.", r"svc\.cluster\.local", r"kube\.calebdunn\.tech", r"nip\.io",
    r"mongodb://", r"redis://", r"local-test-only", r"pk_[0-9a-f]{40,}", r"cash-drugs\.drugs", r":8083",
]


def test_ac010_no_private_operational_detail():
    files = [p for p in WIKI.rglob("*") if p.is_file() and p.suffix in {".md", ".json", ".yml", ".yaml"}]
    files.append(ROOT / "mkdocs.yml")
    for f in files:
        text = f.read_text()
        for pattern in PRIVATE:
            assert not re.search(pattern, text), f"{f.relative_to(ROOT)} contains private detail /{pattern}/"


# AC-011
def test_ac011_container_serves_unprivileged_on_8080_with_healthz():
    dockerfile = (ROOT / "Dockerfile").read_text()
    assert "nginx-unprivileged" in dockerfile and "EXPOSE 8080" in dockerfile
    assert "location = /healthz" in (ROOT / "nginx.conf").read_text()


# AC-012
def test_ac012_faq_covers_common_failures():
    faq = read("help/faq.md")
    for item in ("401", "403", "429", "502", "NDC"):
        assert item in faq


# AC-009: strict build (broken links, missing nav, bad macros fail)
def test_ac009_strict_build():
    result = subprocess.run(
        [sys.executable, "-m", "mkdocs", "build", "--strict", "--site-dir", str(ROOT / "site")],
        cwd=ROOT, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr[-3000:]
