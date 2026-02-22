# 律宝 Web

律宝小队法律智能助手 Web 应用，包含前端界面、后端 API 与 AI 法律问答能力。

## 项目结构

```
律宝web/
├── backend/          # FastAPI 后端
│   ├── app/
│   │   ├── api/      # 接口路由与端点
│   │   ├── core/     # 配置、响应封装
│   │   ├── db/       # 数据库会话
│   │   ├── models/   # ORM 模型
│   │   ├── schemas/  # Pydantic 模型
│   │   └── services/ # 业务逻辑
│   └── requirements.txt
├── frontend/         # Vue 3 + Vite 前端
│   ├── src/
│   │   ├── views/    # 页面组件
│   │   ├── components/
│   │   └── services/ # API 调用
│   └── package.json
├── agent/            # AI 法律问答（RAG + Qwen）
│   ├── scripts/
│   └── requirements.txt
└── README.md
```

## 功能概述

| 模块 | 功能 |
|------|------|
| **前端** | 案件管理、律师展示、AI 法律问答、合规审查、知识库浏览等 |
| **后端** | 用户认证、案件 CRUD、文件上传、法条/合同查询、AI 问答接口 |
| **Agent** | 基于 Qwen 模型 + RAG 的法律知识检索与问答（可接入后端） |

## 快速开始

### 1. 后端

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- API 文档：<http://localhost:8000/docs>
- 健康检查：<http://localhost:8000/health>

### 2. 前端

```bash
cd frontend
npm install
npm run dev
```

- 访问：<http://localhost:3000>

### 3. Agent（可选）

本地法律问答 RAG 推理，需 GPU 或较多内存：

```bash
cd agent
pip install -r requirements.txt
python scripts/agent_rag_qwen.py --query "公司设立需要哪些材料？"
```

## 配置说明

### 后端 (`backend/.env`)

可选创建 `.env` 覆盖默认配置：

| 变量 | 说明 | 默认 |
|------|------|------|
| `DATABASE_URL` | 数据库连接 | `sqlite:///./app.db` |
| `SECRET_KEY` | JWT 签名密钥 | `dev-secret-change-me` |
| `BACKEND_CORS_ORIGINS` | CORS 允许源 | `["http://localhost:3000", ...]` |
| `UPLOAD_DIR` | 上传目录 | `./uploads` |

### 前端

API 基址在 `frontend/src/services/api.ts`：

```ts
const API_BASE_URL = 'http://localhost:8000/api/v1';
```

生产环境建议通过环境变量或构建配置注入。

### 认证

- 登录：`POST /api/v1/auth/login`，返回 `access_token`
- 前端需将 token 存入 `localStorage.setItem('access_token', token)`
- 后续请求会自动携带 `Authorization: Bearer <token>`

## 主要接口

| 路径 | 方法 | 说明 |
|------|------|------|
| `/api/v1/health` | GET | 健康检查 |
| `/api/v1/auth/login` | POST | 登录 |
| `/api/v1/auth/register` | POST | 注册 |
| `/api/v1/cases/legal-cases` | GET | 案件列表 |
| `/api/v1/cases/filters` | GET | 案件过滤选项 |
| `/api/v1/ai/ask` | POST | AI 法律问答 |
| `/api/v1/query/laws` | GET | 法条搜索 |

## 技术栈

- **前端**：Vue 3、Vite、Vue Router、TypeScript
- **后端**：FastAPI、SQLAlchemy、Pydantic、JWT
- **Agent**：PyTorch、Transformers、Qwen、RAG

## License

私有项目，未授权禁止使用。
