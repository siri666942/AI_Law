#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WEB_URL="${WEB_URL:-https://127.0.0.1:8443}"
HEALTHCHECK_RETRIES="${HEALTHCHECK_RETRIES:-30}"
HEALTHCHECK_INTERVAL="${HEALTHCHECK_INTERVAL:-2}"
AI_SMOKE_QUESTION="${AI_SMOKE_QUESTION:-请用 Markdown 简要说明劳动合同中最常见的三类风险。}"
AI_SMOKE_TIMEOUT="${AI_SMOKE_TIMEOUT:-90}"

log() {
  printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*"
}

wait_for_url() {
  local url="$1"
  local name="$2"
  local attempt

  for attempt in $(seq 1 "${HEALTHCHECK_RETRIES}"); do
    if curl -kfsS "${url}" >/dev/null 2>&1; then
      log "${name} 已就绪: ${url}"
      return 0
    fi

    log "等待 ${name} 启动 (${attempt}/${HEALTHCHECK_RETRIES})..."
    sleep "${HEALTHCHECK_INTERVAL}"
  done

  log "${name} 启动失败: ${url}"
  return 1
}

log "进入项目目录: ${PROJECT_ROOT}"
cd "${PROJECT_ROOT}"

log "开始重新构建并启动容器"
docker compose down --remove-orphans
docker compose up -d --build

log "检查前端入口"
wait_for_url "${WEB_URL}/" "前端服务"

log "检查后端健康状态"
wait_for_url "${WEB_URL}/api/v1/health" "后端 API"

log "执行 AI 冒烟测试"
AI_RESPONSE_FILE="$(mktemp)"
HTTP_CODE="$(curl -kssS -o "${AI_RESPONSE_FILE}" -w '%{http_code}' \
  --max-time "${AI_SMOKE_TIMEOUT}" \
  -X POST "${WEB_URL}/api/v1/ai/ask" \
  -H 'Content-Type: application/json' \
  --data "{\"question\":\"${AI_SMOKE_QUESTION}\"}")"

if [[ "${HTTP_CODE}" != "200" ]]; then
  log "AI 接口验证失败，HTTP 状态码: ${HTTP_CODE}"
  cat "${AI_RESPONSE_FILE}"
  rm -f "${AI_RESPONSE_FILE}"
  exit 1
fi

if ! grep -q '"answer"' "${AI_RESPONSE_FILE}"; then
  log "AI 接口返回中未找到 answer 字段"
  cat "${AI_RESPONSE_FILE}"
  rm -f "${AI_RESPONSE_FILE}"
  exit 1
fi

log "AI 冒烟测试通过"
cat "${AI_RESPONSE_FILE}"
rm -f "${AI_RESPONSE_FILE}"

log "执行 AI 流式接口冒烟测试"
AI_STREAM_FILE="$(mktemp)"
HTTP_CODE="$(curl -kssS -N -o "${AI_STREAM_FILE}" -w '%{http_code}' \
  --max-time "${AI_SMOKE_TIMEOUT}" \
  -X POST "${WEB_URL}/api/v1/ai/ask/stream" \
  -H 'Content-Type: application/json' \
  --data "{\"question\":\"${AI_SMOKE_QUESTION}\"}")"

if [[ "${HTTP_CODE}" != "200" ]]; then
  log "AI 流式接口验证失败，HTTP 状态码: ${HTTP_CODE}"
  cat "${AI_STREAM_FILE}"
  rm -f "${AI_STREAM_FILE}"
  exit 1
fi

if ! grep -q '"type": "chunk"\|"type":"chunk"' "${AI_STREAM_FILE}"; then
  log "AI 流式接口返回中未找到 chunk 事件"
  cat "${AI_STREAM_FILE}"
  rm -f "${AI_STREAM_FILE}"
  exit 1
fi

if ! grep -q '"type": "done"\|"type":"done"' "${AI_STREAM_FILE}"; then
  log "AI 流式接口返回中未找到 done 事件"
  cat "${AI_STREAM_FILE}"
  rm -f "${AI_STREAM_FILE}"
  exit 1
fi

log "AI 流式接口冒烟测试通过"
cat "${AI_STREAM_FILE}"
rm -f "${AI_STREAM_FILE}"

log "重新部署完成"
