#!/usr/bin/env bash
# Build a fully static copy of the IELTS Mock Lab (no API, no database).
# Usage: bash scripts/export-static.sh
# Optional: BASE_PATH=/ielts-mock-lab (must match the GitHub Pages project path)
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
base_path="${BASE_PATH:-/ielts-mock-lab}"

if [[ ! "${base_path}" =~ ^/[A-Za-z0-9._-]+$ ]]; then
  echo "BASE_PATH must be a single project path such as /ielts-mock-lab" >&2
  exit 1
fi

echo "Preparing exam data…"
node "${root}/scripts/prepare-static-data.mjs"

echo "Building static site with base path ${base_path}…"
NEXT_PUBLIC_STATIC_MODE=1 NEXT_PUBLIC_BASE_PATH="${base_path}" \
  pnpm --dir "${root}/apps/web" build

out="${root}/apps/web/out"
case "${out}" in
  "${root}/apps/web/out") ;;
  *) echo "Refusing to remove unexpected output path: ${out}" >&2; exit 1 ;;
esac
rm -rf "${out}"
cp -R "${root}/apps/web/.next-static" "${out}"
rm -rf "${out}/cache"
touch "${out}/.nojekyll"

preview="${root}/apps/web/.static-preview"
rm -rf "${preview}"
mkdir -p "${preview}"
ln -s ../out "${preview}${base_path}"

echo "Static site exported to ${out}"
echo "Preview: python3 -m http.server 4173 --directory ${preview}"
echo "Then open: http://127.0.0.1:4173${base_path}/"
