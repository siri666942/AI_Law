"""
=============================================================================
文件: app/api/endpoints/ai.py
模块: AI 智能助手接口
描述: 法律问答、文档生成等 AI 能力，与前端 AIView / agent 对接
=============================================================================
"""

import json
from pathlib import Path
from typing import Any, AsyncIterator

import httpx
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field
from starlette.responses import StreamingResponse

from app.core.config import settings

router = APIRouter()


class AskIn(BaseModel):
    """法律问答请求体"""
    question: str = Field(..., min_length=1, max_length=2000)


class AskOut(BaseModel):
    """法律问答响应"""
    answer: str


class GenerateDocumentIn(BaseModel):
    """文档生成请求体"""
    template_id: str = Field(..., alias="templateId", min_length=1, max_length=100)
    template_name: str = Field(..., alias="templateName", min_length=1, max_length=100)
    user_prompt: str | None = Field(default=None, alias="userPrompt", max_length=2000)


class GenerateDocumentOut(BaseModel):
    """文档生成响应"""
    title: str
    content: str


class ReviewRisk(BaseModel):
    """合规审查风险项"""
    level: str
    text: str


class ReviewDocumentOut(BaseModel):
    """合规审查响应"""
    summary: str
    risks: list[ReviewRisk]
    suggestions: list[str]


def _ensure_llm_configured() -> None:
    if not settings.AI_API_KEY or settings.AI_API_KEY == "__PLACEHOLDER__":
        raise HTTPException(status_code=500, detail="AI_API_KEY 未配置，后端无法调用模型。")
    if not settings.AI_BASE_URL or settings.AI_BASE_URL == "__PLACEHOLDER__":
        raise HTTPException(status_code=500, detail="AI_BASE_URL 未配置，后端无法调用模型。")
    if not settings.AI_MODEL or settings.AI_MODEL == "__PLACEHOLDER__":
        raise HTTPException(status_code=500, detail="AI_MODEL 未配置，后端无法调用模型。")


def _extract_answer(data: dict[str, Any]) -> str:
    choices = data.get("choices")
    if isinstance(choices, list) and choices:
        first_choice = choices[0] or {}
        message = first_choice.get("message")
        if isinstance(message, dict):
            content = message.get("content")
            if isinstance(content, str) and content.strip():
                return content.strip()
            if isinstance(content, list):
                text_parts: list[str] = []
                for item in content:
                    if isinstance(item, dict):
                        text = item.get("text")
                        if isinstance(text, str) and text.strip():
                            text_parts.append(text.strip())
                if text_parts:
                    return "\n".join(text_parts)

        text = first_choice.get("text")
        if isinstance(text, str) and text.strip():
            return text.strip()

    output = data.get("output")
    if isinstance(output, list):
        text_parts: list[str] = []
        for item in output:
            if not isinstance(item, dict):
                continue
            content = item.get("content")
            if not isinstance(content, list):
                continue
            for part in content:
                if isinstance(part, dict):
                    text = part.get("text")
                    if isinstance(text, str) and text.strip():
                        text_parts.append(text.strip())
        if text_parts:
            return "\n".join(text_parts)

    raise HTTPException(status_code=502, detail="模型接口返回成功，但未找到可用回复内容。")


def _extract_stream_delta(data: dict[str, Any]) -> str:
    choices = data.get("choices")
    if isinstance(choices, list) and choices:
        first_choice = choices[0] or {}
        delta = first_choice.get("delta")
        if isinstance(delta, dict):
            content = delta.get("content")
            if isinstance(content, str):
                return content
            if isinstance(content, list):
                text_parts: list[str] = []
                for item in content:
                    if not isinstance(item, dict):
                        continue
                    text = item.get("text")
                    if isinstance(text, str):
                        text_parts.append(text)
                return "".join(text_parts)

    output = data.get("output")
    if isinstance(output, list):
        text_parts: list[str] = []
        for item in output:
            if not isinstance(item, dict):
                continue
            content = item.get("content")
            if not isinstance(content, list):
                continue
            for part in content:
                if not isinstance(part, dict):
                    continue
                text = part.get("text")
                if isinstance(text, str):
                    text_parts.append(text)
        return "".join(text_parts)

    return ""


def _call_llm(messages: list[dict[str, str]], *, response_format: dict[str, str] | None = None) -> str:
    _ensure_llm_configured()

    base_url = settings.AI_BASE_URL.rstrip("/")
    request_body: dict[str, Any] = {
        "model": settings.AI_MODEL,
        "messages": messages,
        "temperature": settings.AI_TEMPERATURE,
        "max_tokens": settings.AI_MAX_TOKENS,
    }
    if response_format is not None:
        request_body["response_format"] = response_format

    headers = {
        "Authorization": f"Bearer {settings.AI_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        with httpx.Client(timeout=settings.AI_TIMEOUT_SECONDS) as client:
            response = client.post(
                f"{base_url}/chat/completions",
                headers=headers,
                json=request_body,
            )
    except httpx.TimeoutException as exc:
        raise HTTPException(status_code=504, detail="模型接口请求超时，请稍后重试。") from exc
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"模型接口请求失败：{exc}") from exc

    if response.status_code >= 400:
        try:
            error_payload = response.json()
        except ValueError:
            error_payload = {"error": {"message": response.text[:500]}}

        error_message = "模型接口调用失败。"
        if isinstance(error_payload, dict):
            error = error_payload.get("error")
            if isinstance(error, dict):
                error_message = str(error.get("message") or error_message)
            elif error:
                error_message = str(error)

        raise HTTPException(
            status_code=502,
            detail=f"模型接口返回异常（HTTP {response.status_code}）：{error_message}",
        )

    try:
        data = response.json()
    except ValueError as exc:
        raise HTTPException(status_code=502, detail="模型接口返回了无法解析的 JSON。") from exc

    return _extract_answer(data)


async def _stream_llm(messages: list[dict[str, str]]) -> AsyncIterator[str]:
    _ensure_llm_configured()

    base_url = settings.AI_BASE_URL.rstrip("/")
    request_body: dict[str, Any] = {
        "model": settings.AI_MODEL,
        "messages": messages,
        "temperature": settings.AI_TEMPERATURE,
        "max_tokens": settings.AI_MAX_TOKENS,
        "stream": True,
    }
    headers = {
        "Authorization": f"Bearer {settings.AI_API_KEY}",
        "Content-Type": "application/json",
    }

    timeout = httpx.Timeout(
        connect=settings.AI_TIMEOUT_SECONDS,
        read=None,
        write=settings.AI_TIMEOUT_SECONDS,
        pool=settings.AI_TIMEOUT_SECONDS,
    )

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            async with client.stream(
                "POST",
                f"{base_url}/chat/completions",
                headers=headers,
                json=request_body,
            ) as response:
                if response.status_code >= 400:
                    try:
                        error_payload = await response.aread()
                        parsed = json.loads(error_payload.decode("utf-8"))
                    except (ValueError, UnicodeDecodeError):
                        parsed = {"error": {"message": "模型接口返回了无法解析的错误信息。"}}

                    error_message = "模型接口调用失败。"
                    if isinstance(parsed, dict):
                        error = parsed.get("error")
                        if isinstance(error, dict):
                            error_message = str(error.get("message") or error_message)
                        elif error:
                            error_message = str(error)

                    raise HTTPException(
                        status_code=502,
                        detail=f"模型接口返回异常（HTTP {response.status_code}）：{error_message}",
                    )

                async for line in response.aiter_lines():
                    if not line:
                        continue
                    if not line.startswith("data:"):
                        continue

                    payload = line[5:].strip()
                    if not payload:
                        continue
                    if payload == "[DONE]":
                        break

                    try:
                        data = json.loads(payload)
                    except json.JSONDecodeError:
                        continue

                    delta = _extract_stream_delta(data)
                    if delta:
                        yield delta
    except httpx.TimeoutException as exc:
        raise HTTPException(status_code=504, detail="模型接口请求超时，请稍后重试。") from exc
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"模型接口请求失败：{exc}") from exc


def _build_messages(question: str) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": (
                "你是“法途”平台的中文 AI 法律助手，服务于中国法律咨询、案件分析、合同审阅和诉讼流程答疑场景。"
                "你的目标是帮助用户快速理解问题、识别风险、明确下一步行动，但不能冒充执业律师、法官或作出生效法律结论。"
                "回答时请遵守以下要求："
                "1. 默认使用简体中文，语气专业、稳健、易懂。"
                "2. 优先围绕中国法律实务场景作答，避免空泛表述。"
                "3. 回答尽量使用 Markdown 排版，优先采用以下结构：`## 结论`、`## 依据与分析`、`## 风险提示`、`## 下一步建议`。"
                "4. 如果用户问题信息不足，请先明确列出缺失事实，再基于常见情形提供条件式分析。"
                "5. 不得编造法条、案号、机构名称、时间线或证据材料；不确定时要明确说明“需进一步核实”。"
                "6. 遇到诉讼时效、管辖、证据保全、合同效力、劳动关系、公司治理、知识产权、借贷担保等问题时，要优先提示程序风险和证据风险。"
                "7. 如果问题涉及明显高风险事项（如即将开庭、拟签署高金额合同、可能违法合规风险），请建议尽快咨询持证律师并补充材料。"
                "8. 除非用户明确要求，否则不要输出冗长免责声明；但结尾要保留必要的风险边界提示。"
            ),
        },
        {"role": "user", "content": question},
    ]


def _build_document_messages(template_name: str, user_prompt: str | None) -> list[dict[str, str]]:
    extra_requirements = user_prompt.strip() if user_prompt else "未补充额外要求，请按标准实务场景生成。"
    return [
        {
            "role": "system",
            "content": (
                "你是“法途”平台的中文法律文书起草助手。"
                "请根据用户指定的文书类型输出一份适合中国法律实务场景的 Markdown 初稿。"
                "要求："
                "1. 输出必须是中文。"
                "2. 内容要完整、结构清晰，适合直接展示在前端页面。"
                "3. 不得编造具体当事人身份信息、案号、日期、金额；未知内容请用“【待补充】”标记。"
                "4. 开头使用一级标题作为文档标题，正文使用二级和三级标题组织。"
                "5. 结尾补充“使用提示”部分，提醒用户根据实际事实和当地要求复核。"
            ),
        },
        {
            "role": "user",
            "content": (
                f"请生成一份“{template_name}”初稿。\n"
                f"额外要求：{extra_requirements}"
            ),
        },
    ]


def _build_review_messages(filename: str, content: str, review_focus: str | None) -> list[dict[str, str]]:
    focus = review_focus.strip() if review_focus else "未指定重点，请进行通用合规性初筛。"
    return [
        {
            "role": "system",
            "content": (
                "你是“法途”平台的中文合同与文档合规审查助手。"
                "请基于用户提供的文档内容进行初步法律风险识别，并严格输出 JSON。"
                '输出格式必须是一个 JSON 对象，且仅包含以下字段：'
                '"summary"（字符串）、"risks"（数组）、"suggestions"（数组）。'
                '"risks" 数组中的每一项必须是包含 "level" 和 "text" 的对象。'
                '"level" 只能是“高”、“中”、“低”。'
                "不得输出 Markdown、代码块标记、解释性前后缀。"
            ),
        },
        {
            "role": "user",
            "content": (
                f"文件名：{filename}\n"
                f"审查重点：{focus}\n"
                "请基于以下文档内容输出结构化审查结果：\n"
                f"{content}"
            ),
        },
    ]


def _strip_markdown_fence(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()
    return cleaned


def _parse_review_payload(raw_text: str) -> ReviewDocumentOut:
    cleaned = _strip_markdown_fence(raw_text)
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=502, detail="模型返回的审查结果不是合法 JSON。") from exc

    if not isinstance(data, dict):
        raise HTTPException(status_code=502, detail="模型返回的审查结果格式不正确。")

    summary = data.get("summary")
    risks = data.get("risks")
    suggestions = data.get("suggestions")
    if not isinstance(summary, str) or not summary.strip():
        raise HTTPException(status_code=502, detail="模型返回的审查摘要缺失或格式不正确。")
    if not isinstance(risks, list):
        raise HTTPException(status_code=502, detail="模型返回的风险列表格式不正确。")
    if not isinstance(suggestions, list):
        raise HTTPException(status_code=502, detail="模型返回的建议列表格式不正确。")

    normalized_risks: list[ReviewRisk] = []
    for item in risks:
        if not isinstance(item, dict):
            raise HTTPException(status_code=502, detail="模型返回的风险项格式不正确。")
        level = item.get("level")
        text = item.get("text")
        if level not in {"高", "中", "低"}:
            raise HTTPException(status_code=502, detail="模型返回了非法风险等级。")
        if not isinstance(text, str) or not text.strip():
            raise HTTPException(status_code=502, detail="模型返回的风险说明缺失或格式不正确。")
        normalized_risks.append(ReviewRisk(level=level, text=text.strip()))

    normalized_suggestions = []
    for item in suggestions:
        if not isinstance(item, str) or not item.strip():
            raise HTTPException(status_code=502, detail="模型返回的建议项格式不正确。")
        normalized_suggestions.append(item.strip())

    return ReviewDocumentOut(
        summary=summary.strip(),
        risks=normalized_risks,
        suggestions=normalized_suggestions,
    )


def _extract_document_title(markdown_text: str, fallback_name: str) -> str:
    for line in markdown_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return f"{fallback_name}初稿"


def _read_uploaded_text(file: UploadFile) -> str:
    suffix = Path(file.filename or "").suffix.lower()
    if suffix != ".txt":
        raise HTTPException(status_code=400, detail="当前暂不支持解析该文件格式，请先转为 txt 后再上传。")

    raw_bytes = file.file.read()
    if not raw_bytes:
        raise HTTPException(status_code=400, detail="上传文件为空，请重新选择文件。")

    try:
        text = raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        try:
            text = raw_bytes.decode("utf-8-sig")
        except UnicodeDecodeError as exc:
            raise HTTPException(status_code=400, detail="txt 文件编码暂不支持，请使用 UTF-8 编码。") from exc

    if not text.strip():
        raise HTTPException(status_code=400, detail="上传文件内容为空，请重新选择文件。")

    return text[:12000]


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
    answer = _call_llm(_build_messages(q))
    return AskOut(answer=answer)


@router.post("/ask/stream")
async def ask_stream(payload: AskIn) -> StreamingResponse:
    q = payload.question.strip()

    async def event_generator() -> AsyncIterator[str]:
        try:
            async for chunk in _stream_llm(_build_messages(q)):
                yield f"data: {json.dumps({'type': 'chunk', 'content': chunk}, ensure_ascii=False)}\n\n"
            yield f"data: {json.dumps({'type': 'done'}, ensure_ascii=False)}\n\n"
        except HTTPException as exc:
            yield (
                f"data: {json.dumps({'type': 'error', 'message': str(exc.detail)}, ensure_ascii=False)}\n\n"
            )
        except Exception:
            yield (
                f"data: {json.dumps({'type': 'error', 'message': '流式回复失败，请稍后重试。'}, ensure_ascii=False)}\n\n"
            )

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.post("/generate-document", response_model=GenerateDocumentOut)
def generate_document(payload: GenerateDocumentIn) -> GenerateDocumentOut:
    """
    AI 文书生成接口

    根据模板类型生成 Markdown 格式的法律文书初稿。
    """
    content = _call_llm(_build_document_messages(payload.template_name, payload.user_prompt))
    title = _extract_document_title(content, payload.template_name)
    return GenerateDocumentOut(title=title, content=content)


@router.post("/review-document", response_model=ReviewDocumentOut)
def review_document(
    file: UploadFile = File(...),
    review_focus: str | None = Form(default=None, alias="reviewFocus"),
) -> ReviewDocumentOut:
    """
    AI 合规审查接口

    当前优先支持 txt 文档，返回结构化风险提示与修改建议。
    """
    file_text = _read_uploaded_text(file)
    raw_result = _call_llm(
        _build_review_messages(file.filename or "未命名文件", file_text, review_focus),
        response_format={"type": "json_object"},
    )
    return _parse_review_payload(raw_result)
