"""
=============================================================================
文件: app/api/endpoints/health.py
模块: 健康检查接口
描述: /api/v1/health，供前端 checkHealth 调用，返回统一包装格式
=============================================================================
"""

from datetime import datetime

from fastapi import APIRouter

router = APIRouter()


@router.get("")
def health() -> dict:
    """
    健康检查（挂载于 /api/v1/health）
    与前端 caseApi.checkHealth() 期望格式一致：{ message, timestamp }
    """
    return {
        "message": "ok",
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
