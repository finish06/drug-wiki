#!/usr/bin/env bash
# Vendor drug-gate's OpenAPI document into the wiki (specs/wiki-v1.md AC-008).
# Usage: scripts/sync-openapi.sh [path-to-drug-gate-checkout]   (default: ../drug-gate)
set -euo pipefail
src="${1:-../drug-gate}/docs/swagger.json"
dest="$(dirname "$0")/../wiki/reference/openapi.json"
python3 - "$src" "$dest" <<'PY'
import json, sys
src, dest = sys.argv[1], sys.argv[2]
spec = json.load(open(src))
# Point "Try it out" at production instead of the generator's default host.
spec["host"] = "drug-gate.calebdunn.tech"
spec["schemes"] = ["https"]
json.dump(spec, open(dest, "w"), indent=2)
open(dest, "a").write("\n")
print(f"vendored {src} -> {dest} ({len(spec['paths'])} paths, v{spec['info']['version']})")
PY
