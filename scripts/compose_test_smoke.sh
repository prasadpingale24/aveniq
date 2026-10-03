#!/usr/bin/env sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
API_URL="${AVENIQ_API_URL:-http://127.0.0.1:8000}"
STANDIN_URL="${CHECKOUT_STANDIN_URL:-http://127.0.0.1:8081}"

echo "Waiting for API at ${API_URL}..."
for i in $(seq 1 30); do
  if python -c "import urllib.request; urllib.request.urlopen('${API_URL}/health')"; then
    break
  fi
  sleep 2
done

echo "Running Playground B03 via scripts/playground_run.py..."
cd "$ROOT"
export AVENIQ_API_URL="$API_URL"
export CHECKOUT_STANDIN_URL="$STANDIN_URL"
python scripts/playground_run.py --scenario b03 --api-base "$API_URL" --standin-base "$STANDIN_URL"

echo "Compose smoke OK"
