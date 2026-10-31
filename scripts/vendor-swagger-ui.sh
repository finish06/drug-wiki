#!/usr/bin/env bash
# Vendor swagger-ui-dist into wiki/assets/swagger-ui/ (specs/zensical-migration.md AC-003).
# Usage: scripts/vendor-swagger-ui.sh [version]   (default 5.17.14)
# Verifies the tarball's sha1 against the npm registry before copying.
set -euo pipefail
version="${1:-5.17.14}"
dest="$(cd "$(dirname "$0")/.." && pwd)/wiki/assets/swagger-ui"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT
curl -fsSL -o "$work/pkg.tgz" "https://registry.npmjs.org/swagger-ui-dist/-/swagger-ui-dist-${version}.tgz"
want="$(curl -fsSL "https://registry.npmjs.org/swagger-ui-dist/${version}" | python3 -c 'import sys,json;print(json.load(sys.stdin)["dist"]["shasum"])')"
got="$(shasum -a 1 "$work/pkg.tgz" | cut -d" " -f1)"
[ "$want" = "$got" ] || { echo "sha1 mismatch: npm $want, downloaded $got" >&2; exit 1; }
tar -xzf "$work/pkg.tgz" -C "$work"
mkdir -p "$dest"
cp "$work/package/swagger-ui-bundle.js" "$work/package/swagger-ui.css" "$work/package/LICENSE" "$dest/"
echo "$version" > "$dest/VERSION"
echo "vendored swagger-ui-dist $version (sha1 $got) -> $dest"
