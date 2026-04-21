# 律宝 Web

律宝小队法律智能助手 Web 应用，包含前端界面、后端 API，以及基于 OpenAI 兼容接口的 AI 法律问答、文档生成和合规审查能力。

当前项目根目录：

```bash
/root/sites/fatu
```

## 项目结构

```
fatu/
├── backend/          # FastAPI 后端
│   ├── app/
│   │   ├── api/      # 接口路由与端点
│   │   ├── core/     # 配置、响应封装
│   │   ├── db/       # 数据库会话
│   │   ├── models/   # ORM 模型
│   │   ├── schemas/  # Pydantic 模型
│   │   └── services/ # 业务逻辑
│   ├── requirements.txt
│   └── README.md
├── frontend/         # Vue 3 + Vite 前端
│   ├── src/
│   │   ├── views/    # 页面组件
│   │   ├── components/
│   │   └── services/ # API 调用
│   └── package.json
├── agent/            # AI 法律问答（RAG + Qwen）
│   ├── scripts/
│   └── requirements.txt
├── scripts/          # 根目录常用启动 / 构建 / 清理脚本
└── README.md
```

## 功能概述

| 模块 | 功能 |
|------|------|
| **前端** | 案件管理、律师展示、AI 法律问答、文档生成、合规审查、知识库浏览等 |
| **后端** | 用户认证、案件 CRUD、文件上传、法条/合同查询、AI 问答 / 文档生成 / 文档审查接口 |
| **Agent** | 基于 Qwen 模型 + RAG 的法律知识检索与问答（可接入后端） |

## 快速开始

### 1. 进入项目目录

```bash
cd /root/sites/fatu
```

### 2. 推荐方式：使用根目录脚本

检查环境：

```bash
./scripts/check_env.sh
```

启动后端：

```bash
./scripts/start_backend.sh
```

启动前端：

```bash
./scripts/start_frontend.sh
```

同时启动前后端：

```bash
./scripts/dev_up.sh
```

更多脚本见 [scripts/README.md](/root/sites/fatu/scripts/README.md)。

### 3. 手动方式

后端：

```bash
cd /root/sites/fatu/backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- API 文档：<http://localhost:8000/docs>
- 健康检查：<http://localhost:8000/health>
- 更多后端说明见 [backend/README.md](/root/sites/fatu/backend/README.md)

前端：

```bash
cd /root/sites/fatu/frontend
npm install
npm run dev
```

- 访问：<http://localhost:5173>

### 4. Agent（可选）

本地法律问答 RAG 推理，需 GPU 或较多内存：

```bash
cd /root/sites/fatu/agent
pip install -r requirements.txt
python scripts/agent_rag_qwen.py --query "公司设立需要哪些材料？"
```

## 常用脚本

根目录 `scripts/` 已整理为常用入口：

| 脚本 | 作用 |
|------|------|
| `./scripts/check_env.sh` | 检查 Python / npm / `.env` / 依赖状态 |
| `./scripts/start_backend.sh` | 启动后端 |
| `./scripts/start_frontend.sh` | 启动前端 |
| `./scripts/dev_up.sh` | 同时启动前后端 |
| `./scripts/build_frontend.sh` | 构建前端 |
| `./scripts/verify_backend.sh` | 运行后端自测和接口验证 |
| `./scripts/ai_smoke_test.sh` | 执行 AI 冒烟测试 |
| `./scripts/clean.sh` | 清理缓存和构建产物 |

## 配置说明

### 后端（项目根 `.env` 或 `backend/.env`）

后端会按以下顺序读取环境文件：

1. `backend/.env`
2. 项目根 `.env`

如果两处都存在，以 `backend/.env` 中的值为准。容器部署可继续直接使用项目根 `.env`。

常用配置如下：

| 变量 | 说明 | 默认 |
|------|------|------|
| `DATABASE_URL` | 数据库连接 | `sqlite:////root/sites/fatu/backend/data/app.db` |
| `SECRET_KEY` | JWT 签名密钥 | `dev-secret-change-me` |
| `BACKEND_CORS_ORIGINS` | CORS 允许源 | 内置若干本地开发地址，必要时请自行覆盖 |
| `UPLOAD_DIR` | 上传目录 | `./uploads` |
| `AI_API_KEY` | 模型接口密钥 | 无 |
| `AI_BASE_URL` | OpenAI 兼容接口地址 | 无 |
| `AI_MODEL` | 模型名 | 无 |
| `AI_TEMPERATURE` | 生成温度 | `0.2` |
| `AI_MAX_TOKENS` | 最大输出长度 | `1024` |
| `AI_TIMEOUT_SECONDS` | 模型请求超时秒数 | `60` |

### 前端

前端默认通过 `frontend/src/services/api.ts` 使用：

```ts
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1';
```

可在项目根 `.env` 中配置：

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

如果留空，则前端默认回落到 `/api/v1`。

如果你本地以前用的是 Vite 默认端口 `5173`，而后端是独立域名或端口访问，请同步检查 `BACKEND_CORS_ORIGINS` 是否包含你的前端地址。

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
| `/api/v1/ai/generate-document` | POST | AI 文档生成 |
| `/api/v1/ai/review-document` | POST | AI 合规审查 |
| `/api/v1/query/laws` | GET | 法条搜索 |

## AI 页面说明

当前 `frontend/src/views/AIView.vue` 中：

- `法律问答`：调用 `/api/v1/ai/ask`
- `文档生成`：调用 `/api/v1/ai/generate-document`
- `合规审查`：调用 `/api/v1/ai/review-document`

其中合规审查当前稳定支持 `.txt` 文件。前端仍允许选择 `.doc`、`.docx`、`.pdf`，但后端会明确提示先转换为 `txt` 后再上传。

## 维护建议

- 优先从项目根 `/root/sites/fatu` 操作，不再使用旧的 `ft_fix/ft_fix/法途` 路径
- 启动、构建、清理尽量走 `scripts/`，减少目录切换带来的错误
- 默认数据库统一为 `/root/sites/fatu/backend/data/app.db`，本地脚本和 Docker 都使用这同一份 SQLite 文件
- 如果 README 与实际命令不一致，优先同步更新根 README、`backend/README.md` 和 `scripts/README.md`

## 技术栈

- **前端**：Vue 3、Vite、Vue Router、TypeScript
- **后端**：FastAPI、SQLAlchemy、Pydantic、JWT
- **Agent**：PyTorch、Transformers、Qwen、RAG

## License

私有项目，未授权禁止使用。
