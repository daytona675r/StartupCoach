#!/usr/bin/env bash
set -euo pipefail

PORT="${PORT:-8502}"
HOST="${HOST:-127.0.0.1}"
BASE_URL="http://${HOST}:${PORT}"

DEMO_MODE=1 streamlit run app.py \
  --server.address="${HOST}" \
  --server.port="${PORT}" \
  --server.headless=true \
  >/tmp/startupcoach-streamlit.log 2>&1 &
PID=$!
trap 'kill "${PID}" 2>/dev/null || true; wait "${PID}" 2>/dev/null || true' EXIT

for _ in $(seq 1 30); do
  if curl --fail --silent --show-error "${BASE_URL}/_stcore/health"; then
    printf '\nStartupCoach demo health check passed.\n'
    exit 0
  fi
  sleep 1
done

echo "StartupCoach demo did not become healthy" >&2
cat /tmp/startupcoach-streamlit.log >&2
exit 1
