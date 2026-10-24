#!/usr/bin/env bash
# Create compose/.env.staging from example with generated secret and prompted login password.
# Run from repo root. Does not print the password.

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
EXAMPLE="$ROOT/compose/.env.staging.example"
TARGET="$ROOT/compose/.env.staging"

if [[ -f "$TARGET" ]]; then
  echo "Already exists: $TARGET (delete or edit manually to re-run)"
  exit 1
fi

if [[ ! -f "$EXAMPLE" ]]; then
  echo "Missing $EXAMPLE"
  exit 1
fi

cp "$EXAMPLE" "$TARGET"
chmod 600 "$TARGET"

SECRET="$(openssl rand -base64 32)"
if [[ "$(uname -s)" == "Darwin" ]]; then
  sed -i '' "s|^AUTH_SESSION_SECRET=.*|AUTH_SESSION_SECRET=${SECRET}|" "$TARGET"
else
  sed -i "s|^AUTH_SESSION_SECRET=.*|AUTH_SESSION_SECRET=${SECRET}|" "$TARGET"
fi

read -r -p "Staging login username [engineer]: " USERNAME
USERNAME="${USERNAME:-engineer}"
read -r -s -p "Staging login password: " PASSWORD
echo
if [[ -z "$PASSWORD" ]]; then
  echo "Password cannot be empty"
  exit 1
fi

# Escape for sed delimiter |
SAFE_PASS="${PASSWORD//|/\\|}"
if [[ "$(uname -s)" == "Darwin" ]]; then
  sed -i '' "s|^AUTH_DEV_USERS=.*|AUTH_DEV_USERS=${USERNAME}:${SAFE_PASS}|" "$TARGET"
else
  sed -i "s|^AUTH_DEV_USERS=.*|AUTH_DEV_USERS=${USERNAME}:${SAFE_PASS}|" "$TARGET"
fi

echo "Wrote $TARGET (mode 600). Start stack:"
echo "  docker compose -f compose/docker-compose.staging.yml --env-file compose/.env.staging up -d --build"
