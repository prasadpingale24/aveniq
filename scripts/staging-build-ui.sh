#!/usr/bin/env bash
# Build aveniq_web and install static files for host nginx.
# Run from repo root. Requires Node 20+ and npm.

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WEB="$ROOT/packages/aveniq_web"
DEST="${AVENIQ_WEB_ROOT:-/var/www/aveniq}"

cd "$WEB"
export VITE_API_BASE_URL=
export VITE_AVENIQ_ENV="${VITE_AVENIQ_ENV:-staging}"

if [[ -f package-lock.json ]]; then
  npm ci
else
  npm install
fi
npm run build

if [[ "$DEST" == "/var/www/aveniq" ]] && [[ ! -w "$(dirname "$DEST")" ]] 2>/dev/null; then
  echo "Installing to $DEST (sudo)..."
  sudo mkdir -p "$DEST"
  sudo rsync -a --delete dist/ "$DEST/"
else
  mkdir -p "$DEST"
  rsync -a --delete dist/ "$DEST/"
fi

echo "UI installed to $DEST"
