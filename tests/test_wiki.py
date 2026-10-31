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


# AC-008 (wiki-v1) / AC-003 (zensical-migration): Swagger UI from vendored assets
def test_ac008_interactive_reference_uses_vendored_swagger_ui():
    api = read("reference/api.md")
    assert 'id="swagger-ui"' in api and "openapi.json" in api
    cfg = load_config()
    for rel in ("assets/swagger-ui/swagger-ui-bundle.js", "assets/javascripts/swagger-init.js"):
        assert rel in cfg["extra_javascript"], f"extra_javascript lacks {rel}"
        assert (WIKI / rel).exists(), f"missing {rel}"
    assert "assets/swagger-ui/swagger-ui.css" in cfg["extra_css"]
    assert (WIKI / "assets/swagger-ui/LICENSE").exists()
    assert json.loads(OPENAPI.read_text())["host"] == "drug-gate.calebdunn.tech"


# AC-009
def test_ac009_config_wiki_practices():
    cfg = load_config()
    features = cfg["theme"]["features"]
    for feature in ("navigation.tabs", "search.suggest", "content.action.edit", "content.code.copy"):
        assert feature in features
    plugin_names = [p if isinstance(p, str) else next(iter(p)) for p in cfg["plugins"]]
    assert "macros" in plugin_names
    # Zensical silently ignores plugins it doesn't support (zensical-migration AC-005).
    assert "swagger-ui-tag" not in plugin_names
    assert cfg["extra"]["api_base"] == "https://drug-gate.calebdunn.tech"
    assert cfg.get("edit_uri") and cfg.get("repo_url")
    for rel in nav_files(cfg["nav"]):
        assert (WIKI / rel).exists(), f"nav points at missing {rel}"
    for page in WIKI.rglob("*.md"):
        if "assets" in page.parts:
            continue
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


# AC-009 (wiki-v1) / AC-001, AC-002, AC-004 (zensical-migration): strict Zensical build
@pytest.fixture(scope="module")
def built_site():
    result = subprocess.run(
        [str(Path(sys.executable).with_name("zensical")), "build", "--strict"],
        cwd=ROOT, capture_output=True, text=True,
    )
    assert result.returncode == 0, (result.stdout + result.stderr)[-3000:]
    return ROOT / "site"


def test_ac009_strict_zensical_build_keeps_urls(built_site):
    for url in ("index.html", "get-started/quickstart/index.html", "guides/interactions/index.html",
                "reference/api/index.html", "reference/openapi.json", "help/faq/index.html"):
        assert (built_site / url).exists(), f"{url} missing from the build"
    quickstart = (built_site / "get-started/quickstart/index.html").read_text()
    assert "https://drug-gate.calebdunn.tech/v1/drugs/info?name=warfarin" in quickstart
    assert "{{ api_base }}" not in quickstart


def test_zensical_ac004_footer_made_with_zensical(built_site):
    index = (built_site / "index.html").read_text()
    assert "Made with" in index and "zensical.org" in index


def test_zensical_ac003_api_page_loads_swagger_assets(built_site):
    api = (built_site / "reference/api/index.html").read_text()
    assert "swagger-ui-bundle.js" in api and "swagger-init.js" in api and "swagger-ui.css" in api


def test_zensical_ac001_requirements_pin_zensical_only():
    reqs = (ROOT / "requirements.txt").read_text()
    assert "zensical==" in reqs
    for gone in ("mkdocs==", "mkdocs-material", "mkdocs-macros-plugin", "mkdocs-swagger-ui-tag"):
        assert gone not in reqs, f"requirements still pins {gone}"


# ---- System section (specs/system-section.md) ----
SYSTEM_PAGES = ["system/index.md", "system/drug-gate.md", "system/cash-drugs.md", "system/rx-dag.md",
                "system/data-freshness.md", "system/reliability.md"]
SERVICE_SECTIONS = ["## What it does", "## How it works", "## Data", "## Interfaces", "## Reliability", "## Source code"]
REPOS = {"system/drug-gate.md": "github.com/finish06/drug-gate",
         "system/cash-drugs.md": "github.com/finish06/cash-drugs",
         "system/rx-dag.md": "github.com/finish06/ndc-loader"}


def test_system_ac001_overview_diagram_services_and_walkthrough():
    text = read("system/index.md")
    # Hand-drawn, theme-aware SVG (replaced the auto-laid-out Mermaid diagram).
    assert '<svg class="dg"' in text and 'role="img"' in text and "<title" in text and "<desc" in text
    assert "\n\n" not in text[text.index("<svg"):text.index("</svg>")], "blank line inside the SVG breaks Markdown"
    for word in ("drug-gate", "cash-drugs", "rx-dag", "DailyMed", "openFDA", "RxNorm"):
        assert word in text, f"overview does not mention {word}"
    assert "## A request, step by step" in text
    for page in ("drug-gate.md", "cash-drugs.md", "rx-dag.md", "data-freshness.md", "reliability.md"):
        assert page in text


@pytest.mark.parametrize("page", ["system/drug-gate.md", "system/cash-drugs.md", "system/rx-dag.md"])
def test_system_ac002_ac005_service_pages_follow_template_and_link_source(page):
    text = read(page)
    positions = [text.find(s) for s in SERVICE_SECTIONS]
    assert all(p >= 0 for p in positions), f"{page} lacks {[s for s, p in zip(SERVICE_SECTIONS, positions) if p < 0]}"
    assert positions == sorted(positions), f"{page} sections out of order"
    assert REPOS[page] in text


def test_system_ac003_freshness_covers_each_data_kind():
    text = read("system/data-freshness.md")
    for kind in ("Drug names", "Drug classes", "NDC", "Product labels", "RxNorm", "Recalls", "Shortages"):
        assert kind in text, f"freshness page lacks {kind}"


def test_system_ac004_reliability_covers_failure_modes():
    text = read("system/reliability.md").lower()
    for item in ("stale", "circuit breaker", "429", "retry", "last good copy", "alert"):
        assert item in text, f"reliability page lacks {item!r}"


def test_system_ac006_nav_and_cross_links():
    cfg = load_config()
    tabs = [next(iter(t)) for t in cfg["nav"] if isinstance(t, dict)]
    assert "System" in tabs
    assert "system/index.md" in read("index.md")
    assert "../system/index.md" in read("get-started/concepts.md")


def test_system_ac007_no_ports_in_system_pages():
    for page in SYSTEM_PAGES:
        assert not re.search(r":\d{4,5}\b", read(page)), f"{page} mentions a port"


# ---- Pipeline deploy (specs/ci-deploy.md) ----
K8S = ROOT / "k8s"


def k8s_docs(rel):
    return [d for d in yaml.safe_load_all((K8S / rel).read_text()) if d]


def test_deploy_ac001_base_matches_live_behavior():
    docs = {d["kind"]: d for d in k8s_docs("base/drug-wiki.yaml")}
    assert set(docs) == {"Deployment", "Service", "PodDisruptionBudget"}
    dep = docs["Deployment"]["spec"]
    assert dep["replicas"] == 2
    pod = dep["template"]["spec"]
    assert pod["securityContext"]["runAsUser"] == 101 and pod["automountServiceAccountToken"] is False
    c = pod["containers"][0]
    assert c["securityContext"]["readOnlyRootFilesystem"] is True
    assert c["readinessProbe"]["httpGet"]["path"] == "/healthz"
    assert c["lifecycle"]["preStop"]["exec"]["command"] == ["sleep", "15"]
    assert {"name": "tmp", "mountPath": "/tmp"} in c["volumeMounts"]
    assert docs["PodDisruptionBudget"]["spec"]["minAvailable"] == 1
    overlay = yaml.safe_load((K8S / "overlays/prod/kustomization.yaml").read_text())
    assert overlay["namespace"] == "drugs"
    assert overlay["images"][0]["name"] == "dockerhub.calebdunn.tech/finish06/drug-wiki"


def test_deploy_ac002_k8s_has_no_private_hosts():
    for f in K8S.rglob("*.yaml"):
        text = f.read_text()
        for pattern in (r"nip\.io", r"\b10\.\d+\.\d+\.\d+", r"192\.168\.", r"svc\.cluster\.local", r"IngressRoute"):
            if f.name == "deployer-rbac.yaml" and pattern == r"svc\.cluster\.local":
                continue
            assert not re.search(pattern, text), f"{f.relative_to(ROOT)} contains /{pattern}/"


def deploy_cmd():
    wf = yaml.safe_load((ROOT / ".gitea/workflows/staging-release.yml").read_text())
    return wf["jobs"]["staging-release"]["steps"][0]["with"]["deploy-cmd"], wf


def test_deploy_ac003_apply_overlay_not_set_image():
    cmd, wf = deploy_cmd()
    assert "kustomize edit set image" in cmd
    assert "kubectl diff" in cmd and "apply -k" in cmd
    assert "rollout status" in cmd and "--timeout=180s" in cmd
    assert "set image deploy" not in cmd


def test_deploy_ac004_rollback_on_failed_rollout():
    cmd, _ = deploy_cmd()
    assert "rollout undo" in cmd


def test_deploy_ac009_diff_errors_fail_and_kubectl_matches_server_minor():
    cmd, _ = deploy_cmd()
    assert "|| true" not in cmd.split("kubectl diff")[1].splitlines()[0]
    assert '"$rc" -gt 1' in cmd
    assert "/release/v1.34." in cmd


def test_deploy_ac010_committed_overlay_pin_has_digest():
    overlay = yaml.safe_load((K8S / "overlays/prod/kustomization.yaml").read_text())
    assert overlay["images"][0]["digest"].startswith("sha256:")


def test_deploy_ac005_smoke_check_and_tag_confirmation():
    cmd, _ = deploy_cmd()
    assert "https://wiki.drugs.calebdunn.tech/healthz" in cmd
    # Operator conditions (2026-10-30): pin by digest; prove every pod runs it.
    assert "docker-content-digest" in cmd and '@${DIGEST}"' in cmd
    assert "imageID" in cmd and "$DIGEST" in cmd
    # Terminating pods (preStop sleep) still report Running with the old image (run 6266).
    assert "deletionTimestamp" in cmd


def test_deploy_ac006_fail_fast_without_secret():
    cmd, wf = deploy_cmd()
    assert 'if [ -z "${WIKI_KUBECONFIG:-}" ]' in cmd and "k8s/deployer-rbac.yaml" in cmd
    env = wf["jobs"]["staging-release"]["steps"][0]["env"]
    assert env["WIKI_KUBECONFIG"] == "${{ secrets.WIKI_KUBECONFIG }}"
    assert "'" not in cmd, "ci-shared single-quotes deploy-cmd: no apostrophes"


def test_deploy_ac007_rbac_is_scoped():
    docs = {d["kind"]: d for d in k8s_docs("deployer-rbac.yaml")}
    assert set(docs) == {"ServiceAccount", "Role", "RoleBinding"}
    for rule in docs["Role"]["rules"]:
        assert not {"create", "delete", "deletecollection", "*"} & set(rule["verbs"]), rule
        if set(rule["resources"]) & {"deployments", "services", "poddisruptionbudgets"} and \
                {"patch", "update"} & set(rule["verbs"]):
            assert rule.get("resourceNames") == ["drug-wiki"], rule
