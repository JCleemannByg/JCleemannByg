#!/usr/bin/env bash
# Local development server. Danish site at http://localhost:1313/.
# Override the port with PORT=1314 ./scripts/dev.sh
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
PORT="${PORT:-1313}"
exec "$HUGO_BIN" server \
  --bind 127.0.0.1 \
  --port "$PORT" \
  --baseURL "http://localhost:${PORT}/" \
  --disableFastRender \
  --printI18nWarnings
