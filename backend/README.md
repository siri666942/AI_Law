# 律宝小队 - 后端（FastAPI）

当前后端目录：

```bash
/root/sites/fatu/backend
```

## 运行环境
- Python 3.10+（推荐 3.11）

## 安装依赖
在 `backend/` 目录下执行：

```bash
python -m pip install -r requirements.txt
```

## 启动服务
在 `backend/` 目录下执行：

```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

启动后：
- Swagger：`http://127.0.0.1:8000/docs`
- OpenAPI：`http://127.0.0.1:8000/openapi.json`

如果你在项目根目录，更推荐直接执行：

```bash
cd /root/sites/fatu
./scripts/start_backend.sh
```

## 环境变量

后端会显式读取两处 `.env`：

1. `backend/.env`
2. 项目根 `.env`

如果两处都存在，`backend/.env` 优先。这样既兼容本地从 `backend/` 目录启动，也兼容项目根目录下的 `docker-compose.yml`。

数据库默认值已统一为：

```bash
sqlite:////root/sites/fatu/backend/data/app.db
```

也就是说，本地脚本启动和 Docker 部署默认都会落到 `backend/data/app.db`，不再因为工作目录不同生成多份 `app.db`。

AI 相关变量：

| 变量 | 说明 |
|------|------|
| `AI_API_KEY` | 模型接口密钥 |
| `AI_BASE_URL` | OpenAI 兼容接口地址，例如 `https://api.openai.com/v1` |
| `AI_MODEL` | 模型名称 |
| `AI_TEMPERATURE` | 生成温度 |
| `AI_MAX_TOKENS` | 最大输出长度 |
| `AI_TIMEOUT_SECONDS` | 请求超时秒数 |

## AI 接口

当前后端提供三类 AI 接口：

| 路径 | 方法 | 说明 |
|------|------|------|
| `/api/v1/ai/ask` | POST | AI 法律问答 |
| `/api/v1/ai/generate-document` | POST | 生成 Markdown 法律文书初稿 |
| `/api/v1/ai/review-document` | POST | 审查上传文档并返回结构化风险结果 |

说明：

- `review-document` 当前优先支持 `.txt`
- 上传其他格式会返回明确错误，提示先转为 `txt`
- AI 成功响应会被统一包装为 `{ success: true, data: ... }`

## 本地自测
先启动服务，再在 `backend/` 目录下执行：

```bash
python scripts/self_test.py
```

如果需要额外验证主要业务接口，可执行：

```bash
python scripts/verify_api.py
```

也可以在项目根目录直接执行：

```bash
cd /root/sites/fatu
./scripts/verify_backend.sh
```

