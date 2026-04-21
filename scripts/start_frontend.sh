#!/usr/bin/env bash

set -euo pipefail

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/common.sh"

HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-5173}"

require_cmd "${NPM_BIN}"
ensure_frontend_deps

log "启动前端: http://${HOST}:${PORT}"
cd "${FRONTEND_DIR}"
exec "${NPM_BIN}" run dev -- --host "${HOST}" --port "${PORT}"
