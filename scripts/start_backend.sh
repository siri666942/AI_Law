#!/usr/bin/env bash

set -euo pipefail

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/common.sh"

HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8000}"

require_cmd "${PYTHON_BIN}"
ensure_backend_deps

log "启动后端: http://${HOST}:${PORT}"
cd "${BACKEND_DIR}"
exec "${PYTHON_BIN}" -m uvicorn app.main:app --reload --host "${HOST}" --port "${PORT}"
