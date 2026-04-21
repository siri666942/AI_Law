#!/usr/bin/env bash

set -euo pipefail

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/common.sh"

require_cmd "${PYTHON_BIN}"
ensure_backend_deps

cd "${BACKEND_DIR}"

log "运行基础自测"
"${PYTHON_BIN}" scripts/self_test.py

log "运行接口验证"
"${PYTHON_BIN}" scripts/verify_api.py

log "后端验证完成"
