#!/usr/bin/env bash
# Production-style local build.
#
#   ./scripts/build.sh                          # local preview at http://localhost:8080/
#   BASE_URL=https://user.github.io/JCleemannByg/ ./scripts/build.sh   # GitHub Pages
#   BASE_URL=https://jcleemannbyg.dk/ ./scripts/build.sh               # custom domain later
#
# Then: python3 scripts/verify.py --public public --base /   (or the matching base path)
set -euo pipefail
cd "$(dirname "$0")/.."
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
if [ -n "${HUGO:-}" ]; then
  HUGO_BIN="$HUGO"
elif [ -x "$ROOT/bin/hugo" ]; then
  HUGO_BIN="$ROOT/bin/hugo"
else
  HUGO_BIN="hugo"
fi
BASE_URL="${BASE_URL:-http://localhost:8080/}"
BASE_PATH="$(printf '%s' "$BASE_URL" | sed -E 's#^[a-z]+://[^/]+##')"
[ -n "$BASE_PATH" ] || BASE_PATH="/"

"$HUGO_BIN" --minify --cleanDestinationDir --baseURL "$BASE_URL"

echo
echo "Built into public/ for ${BASE_URL}"
echo "Verify with:  python3 scripts/verify.py --public public --base ${BASE_PATH}"
