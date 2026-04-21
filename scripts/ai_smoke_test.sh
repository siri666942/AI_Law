#!/usr/bin/env bash

set -euo pipefail

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/common.sh"

require_cmd "${PYTHON_BIN}"

BACKEND_BASE_URL="${BACKEND_BASE_URL:-http://127.0.0.1:8000}"
QUESTION="${QUESTION:-请用 Markdown 简要说明劳动合同中最常见的三类风险。}"

log "检查后端健康状态: ${BACKEND_BASE_URL}/health"
"${PYTHON_BIN}" - <<'PY' "${BACKEND_BASE_URL}"
import sys
import urllib.request

base_url = sys.argv[1].rstrip("/")
with urllib.request.urlopen(f"{base_url}/health", timeout=5) as response:
    if response.status != 200:
        raise SystemExit(f"健康检查失败: HTTP {response.status}")
print("health ok")
PY

log "执行 AI 冒烟测试"
"${PYTHON_BIN}" - <<'PY' "${BACKEND_BASE_URL}" "${QUESTION}"
import json
import sys
import urllib.error
import urllib.request

base_url = sys.argv[1].rstrip("/")
question = sys.argv[2]
payload = json.dumps({"question": question}).encode("utf-8")
request = urllib.request.Request(
    f"{base_url}/api/v1/ai/ask",
    data=payload,
    headers={"Content-Type": "application/json"},
    method="POST",
)

try:
    with urllib.request.urlopen(request, timeout=60) as response:
        body = response.read().decode("utf-8")
        print(body)
        data = json.loads(body)
except urllib.error.HTTPError as exc:
    detail = exc.read().decode("utf-8", errors="replace")
    raise SystemExit(f"AI 冒烟测试失败: HTTP {exc.code} {detail}") from exc

answer = None
if isinstance(data, dict):
    if isinstance(data.get("answer"), str):
        answer = data["answer"]
    elif isinstance(data.get("data"), dict) and isinstance(data["data"].get("answer"), str):
        answer = data["data"]["answer"]

if not answer or not answer.strip():
    raise SystemExit("AI 接口返回成功，但未找到有效 answer 字段。")

print("\nAI smoke test passed.")
PY
