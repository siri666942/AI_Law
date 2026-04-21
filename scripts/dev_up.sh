#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

BACKEND_HOST="${BACKEND_HOST:-127.0.0.1}"
BACKEND_PORT="${BACKEND_PORT:-8000}"
FRONTEND_HOST="${FRONTEND_HOST:-127.0.0.1}"
FRONTEND_PORT="${FRONTEND_PORT:-5173}"

backend_pid=""
frontend_pid=""

cleanup() {
  local exit_code=$?
  if [[ -n "${backend_pid}" ]] && kill -0 "${backend_pid}" >/dev/null 2>&1; then
    log "停止后端进程 ${backend_pid}"
    kill "${backend_pid}" >/dev/null 2>&1 || true
  fi
  if [[ -n "${frontend_pid}" ]] && kill -0 "${frontend_pid}" >/dev/null 2>&1; then
    log "停止前端进程 ${frontend_pid}"
    kill "${frontend_pid}" >/dev/null 2>&1 || true
  fi
  exit "${exit_code}"
}

trap cleanup INT TERM EXIT

require_cmd "${PYTHON_BIN}"
require_cmd "${NPM_BIN}"
ensure_backend_deps
ensure_frontend_deps

log "并行启动前后端"
HOST="${BACKEND_HOST}" PORT="${BACKEND_PORT}" "${SCRIPT_DIR}/start_backend.sh" &
backend_pid=$!

HOST="${FRONTEND_HOST}" PORT="${FRONTEND_PORT}" "${SCRIPT_DIR}/start_frontend.sh" &
frontend_pid=$!

log "后端 PID: ${backend_pid}"
log "前端 PID: ${frontend_pid}"
log "按 Ctrl+C 可同时停止"

wait -n "${backend_pid}" "${frontend_pid}"
