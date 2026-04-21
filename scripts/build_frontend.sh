#!/usr/bin/env bash

set -euo pipefail

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/common.sh"

require_cmd "${NPM_BIN}"
ensure_frontend_deps

cd "${FRONTEND_DIR}"
log "开始构建前端"
exec "${NPM_BIN}" run build
