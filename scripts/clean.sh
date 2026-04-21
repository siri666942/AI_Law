#!/usr/bin/env bash

set -euo pipefail

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/common.sh"

MODE="${1:-safe}"

show_usage() {
  cat <<'EOF'
用法:
  ./scripts/clean.sh            # 默认 safe 模式
  ./scripts/clean.sh safe       # 清理缓存和构建产物
  ./scripts/clean.sh all        # 在 safe 基础上额外清理依赖目录

说明:
  safe: 删除 __pycache__、.pytest_cache、htmlcov、frontend/dist、backend/uploads 下的临时文件
  all : 额外删除 frontend/node_modules、frontend/.vite
EOF
}

if [[ "${MODE}" != "safe" && "${MODE}" != "all" ]]; then
  show_usage
  exit 1
fi

log "开始清理 (${MODE})"

find "${PROJECT_ROOT}" \
  \( -path "${PROJECT_ROOT}/.git" -o -path "${PROJECT_ROOT}/frontend/node_modules" -o -path "${PROJECT_ROOT}/myenv" \) -prune \
  -o \
  \( -type d \( -name "__pycache__" -o -name ".pytest_cache" -o -name "htmlcov" -o -name ".tox" \) -print -exec rm -rf {} + \)

if [[ -d "${FRONTEND_DIR}/dist" ]]; then
  log "删除前端构建目录: ${FRONTEND_DIR}/dist"
  rm -rf "${FRONTEND_DIR}/dist"
fi

if [[ -d "${FRONTEND_DIR}/.vite" ]]; then
  log "删除前端缓存目录: ${FRONTEND_DIR}/.vite"
  rm -rf "${FRONTEND_DIR}/.vite"
fi

if [[ -d "${BACKEND_DIR}/uploads" ]]; then
  log "清理后端上传目录中的临时文件"
  find "${BACKEND_DIR}/uploads" -mindepth 1 -maxdepth 1 -type f -print -delete
fi

if [[ "${MODE}" == "all" ]]; then
  if [[ -d "${FRONTEND_DIR}/node_modules" ]]; then
    log "删除前端依赖目录: ${FRONTEND_DIR}/node_modules"
    rm -rf "${FRONTEND_DIR}/node_modules"
  fi
fi

log "清理完成"
