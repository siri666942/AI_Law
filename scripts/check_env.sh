#!/usr/bin/env bash

set -euo pipefail

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/common.sh"

log "项目根目录: ${PROJECT_ROOT}"
log "后端目录: ${BACKEND_DIR}"
log "前端目录: ${FRONTEND_DIR}"

if command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  log "Python: $("${PYTHON_BIN}" --version 2>&1)"
else
  printf 'Python 不可用\n' >&2
  exit 1
fi

if command -v "${NPM_BIN}" >/dev/null 2>&1; then
  log "NPM: $("${NPM_BIN}" --version)"
else
  printf 'npm 不可用\n' >&2
  exit 1
fi

if [[ -f "${PROJECT_ROOT}/.env" ]]; then
  log "检测到项目根 .env"
else
  log "未检测到项目根 .env"
fi

if [[ -f "${BACKEND_DIR}/.env" ]]; then
  log "检测到 backend/.env"
else
  log "未检测到 backend/.env"
fi

if [[ -d "${FRONTEND_DIR}/node_modules" ]]; then
  log "前端依赖目录已存在"
else
  log "前端依赖目录不存在"
fi

if "${PYTHON_BIN}" -c "import fastapi, uvicorn, httpx, pydantic_settings" >/dev/null 2>&1; then
  log "后端 Python 依赖已就绪"
else
  log "后端 Python 依赖未完全安装"
fi
