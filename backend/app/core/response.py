"""
=============================================================================
文件: app/core/response.py
模块: 统一响应格式
描述: 为前端兼容，将 API 响应统一包装为 { success, data } 格式
=============================================================================
"""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
import json


class ApiResponseWrapper(BaseHTTPMiddleware):
    """
    中间件：将 /api/v1 下的成功响应包装为 { success: true, data: ... }
    前端期望此格式，不修改前端解析逻辑。
    """

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # 仅处理 /api/v1 下的 JSON 响应
        if not request.url.path.startswith("/api/v1"):
            return response

        # 仅包装 2xx 成功响应
        if response.status_code < 200 or response.status_code >= 300:
            return response

        # 仅处理 application/json
        content_type = response.headers.get("content-type", "")
        if "application/json" not in content_type:
            return response

        try:
            body = b""
            async for chunk in response.body_iterator:
                body += chunk
            data = json.loads(body.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return response

        wrapped = {"success": True, "data": data}
        return JSONResponse(content=wrapped, status_code=response.status_code)
