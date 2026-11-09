#!/usr/bin/env bash
# Local development server. Danish site at http://localhost:1313/, English at /en/.
# Override the port with PORT=1314 ./scripts/dev.sh
set -euo pipefail
cd "$(dirname "$0")/.."
HUGO_BIN="${HUGO:-hugo}"
PORT="${PORT:-1313}"
exec "$HUGO_BIN" server \
  --bind 127.0.0.1 \
  --port "$PORT" \
  --baseURL "http://localhost:${PORT}/" \
  --disableFastRender \
  --printI18nWarnings
