#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_DIR="${PROJECT_ROOT}/backend"
FRONTEND_DIR="${PROJECT_ROOT}/frontend"

PYTHON_BIN="${PYTHON_BIN:-python3}"
if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  PYTHON_BIN="${PYTHON_BIN:-python}"
fi

NPM_BIN="${NPM_BIN:-npm}"

log() {
  printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*"
}

require_cmd() {
  local cmd="$1"
  if ! command -v "${cmd}" >/dev/null 2>&1; then
    printf '缺少命令: %s\n' "${cmd}" >&2
    exit 1
  fi
}

ensure_backend_deps() {
  if ! "${PYTHON_BIN}" -c "import fastapi, uvicorn, httpx, pydantic_settings" >/dev/null 2>&1; then
    printf '后端依赖未准备好，请先执行: cd %s && %s -m pip install -r requirements.txt\n' "${BACKEND_DIR}" "${PYTHON_BIN}" >&2
    exit 1
  fi
}

ensure_frontend_deps() {
  if [[ ! -d "${FRONTEND_DIR}/node_modules" ]]; then
    printf '前端依赖未安装，请先执行: cd %s && %s install\n' "${FRONTEND_DIR}" "${NPM_BIN}" >&2
    exit 1
  fi
}
