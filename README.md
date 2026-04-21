# 法途 
访问地址：https://85.121.122.124:8443/
法途是一个法律服务 Web 应用，当前主线包含：

- Vue 3 + Vite 前端
- FastAPI 后端 API
- 基于 OpenAI 兼容接口的 AI 法律问答、文档生成、文档审查
- 用户注册 / 登录 / JWT 鉴权
- Docker Compose 一键重部署

## 当前结构

```text
fatu/
├── backend/            # FastAPI 后端
├── frontend/           # Vue 3 前端
├── agent/              # 法律问答 / RAG 相关脚本与数据
├── deploy/             # Nginx / Docker 部署配置
├── scripts/            # 启动、检查、重部署脚本
├── docker-compose.yml
└── README.md
```

## 当前功能

- 首页、知识库、法律流程、智能诊断、项目空间等前端页面
- 登录 / 注册页面：`/login`
- AI 助手页面：
  - 法律问答
  - 文档生成
  - 合规审查
- 后端统一 API 前缀：`/api/v1`
- JWT 登录态，前端存储在 `localStorage`

## 技术栈

- 前端：Vue 3、Vue Router、TypeScript、Vite、Markdown-It
- 后端：FastAPI、SQLAlchemy、Pydantic、JWT、HTTPX
- 部署：Docker Compose、Nginx
- AI：OpenAI 兼容接口，可接 Qwen / 其他兼容模型

## 本地开发

### 进入项目

```bash
cd /root/sites/fatu
```

### 前端

```bash
cd frontend
npm install
npm run dev
```

默认开发地址：

- 前端：<http://localhost:5173>

### 后端

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

默认开发地址：

- API：<http://localhost:8000>
- Swagger：<http://localhost:8000/docs>
- 健康检查：<http://localhost:8000/health>

## 部署与上线

当前线上主流程以 Docker Compose 为准：

```bash
cd /root/sites/fatu
bash scripts/redeploy.sh
```

这个脚本会执行：

1. `docker compose down --remove-orphans`
2. `docker compose up -d --build`
3. 检查前端首页可访问
4. 检查 `/api/v1/health`
5. 执行 AI 普通接口冒烟测试
6. 执行 AI 流式接口冒烟测试

默认对外访问地址：

- 前端：`https://127.0.0.1:8443/`
- 后端健康检查：`https://127.0.0.1:8443/api/v1/health`

## 环境变量

项目根 `.env` 会被 Docker Compose 直接加载。

后端当前主要依赖这些变量：

| 变量 | 说明 |
|------|------|
| `DATABASE_URL` | 数据库连接串 |
| `SECRET_KEY` | JWT 签名密钥 |
| `BACKEND_CORS_ORIGINS` | 允许的前端来源 |
| `UPLOAD_DIR` | 上传目录 |
| `AI_API_KEY` | 模型接口密钥 |
| `AI_BASE_URL` | OpenAI 兼容接口地址 |
| `AI_MODEL` | 模型名称 |
| `AI_TEMPERATURE` | 温度 |
| `AI_MAX_TOKENS` | 最大输出长度 |
| `AI_TIMEOUT_SECONDS` | 超时秒数 |

前端接口基址：

```ts
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1'
```

如需本地直连后端，可在环境中设置：

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

## 主要接口

| 路径 | 方法 | 说明 |
|------|------|------|
| `/api/v1/health` | GET | 健康检查 |
| `/api/v1/auth/register` | POST | 注册并返回 token + user |
| `/api/v1/auth/login` | POST | 登录并返回 token + user |
| `/api/v1/auth/me` | GET | 当前登录用户 |
| `/api/v1/ai/ask` | POST | AI 问答 |
| `/api/v1/ai/ask/stream` | POST | AI 流式问答 |
| `/api/v1/ai/generate-document` | POST | 文档生成 |
| `/api/v1/ai/review-document` | POST | 文档审查 |
| `/api/v1/cases/legal-cases` | GET | 案件列表 |
| `/api/v1/cases/filters` | GET | 案件筛选项 |
| `/api/v1/query/laws` | GET | 法条查询 |

## 认证说明

- 登录和注册都会返回 `access_token + user`
- 前端通过 `frontend/src/services/api.ts` 中的 `authApi` 管理会话
- token 保存键：`access_token`
- 用户信息保存键：`user_info`

当前角色以主线为准：

- `lawyer`
- `client`

后端对旧前端传入的 `user` 角色做了兼容映射，会自动转成 `client`

## 说明与约束

- 主线以 `fatu` 目录为准，不再参考旧路径或旧压缩包内的历史 README
- AI 页面当前已经接入真实后端能力，不要再用早期占位版页面覆盖
- 部署脚本、README、接口行为应保持同步更新

## 相关文件

- 根部署脚本：[scripts/redeploy.sh](/root/sites/fatu/scripts/redeploy.sh)
- 后端入口：[backend/app/main.py](/root/sites/fatu/backend/app/main.py)
- 路由汇总：[backend/app/api/router.py](/root/sites/fatu/backend/app/api/router.py)
- 前端接口封装：[frontend/src/services/api.ts](/root/sites/fatu/frontend/src/services/api.ts)
- 登录页：[frontend/src/views/LoginView.vue](/root/sites/fatu/frontend/src/views/LoginView.vue)

## License

私有项目，未授权禁止分发和商用。
