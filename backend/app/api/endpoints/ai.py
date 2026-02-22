"""
=============================================================================
文件: app/api/endpoints/ai.py
模块: AI 智能助手接口
描述: 法律问答、文档生成等 AI 能力，与前端 AIView / agent 对接
=============================================================================
"""

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()


class AskIn(BaseModel):
    """法律问答请求体"""
    question: str = Field(..., min_length=1, max_length=2000)


class AskOut(BaseModel):
    """法律问答响应"""
    answer: str


@router.post("/ask", response_model=AskOut)
def ask(payload: AskIn) -> AskOut:
    """
    AI 法律问答接口
    
    【功能说明】
    接收用户法律问题，返回 AI 分析回答。
    当前为占位实现，可按需接入 LLM / RAG（如 agent 的 Qwen 模型）。
    
    【请求体】
    - question: str - 用户提出的法律问题
    
    【返回值】
    - answer: str - AI 生成的回答
    """
    q = payload.question.strip()
    # 占位：返回简单回复，实际可接入 agent_rag_qwen 或外部 LLM
    answer = (
        f"您的问题：「{q[:50]}{'...' if len(q) > 50 else ''}」\n\n"
        "当前为占位回复。如需真实 AI 能力，可配置 LLM 并在此处调用。"
        "建议：1) 接入 agent 的 RAG 流程；2) 或调用 OpenAI/通义等 API。"
    )
    return AskOut(answer=answer)
