# Scripts

根目录常用脚本，统一从项目根调用，不需要手动切换到 `backend/` 或 `frontend/`。

## 常用命令

```bash
cd /root/sites/fatu
```

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

构建前端：

```bash
./scripts/build_frontend.sh
```

跑后端自测和接口验证：

```bash
./scripts/verify_backend.sh
```

AI 冒烟测试：

```bash
./scripts/ai_smoke_test.sh
```

清理缓存和构建产物：

```bash
./scripts/clean.sh
```

彻底清理到需要重新安装前端依赖：

```bash
./scripts/clean.sh all
```

## 可选环境变量

启动脚本支持临时覆盖端口或命令：

```bash
HOST=0.0.0.0 PORT=9000 ./scripts/start_backend.sh
HOST=0.0.0.0 PORT=5174 ./scripts/start_frontend.sh
BACKEND_PORT=9000 FRONTEND_PORT=5174 ./scripts/dev_up.sh
PYTHON_BIN=python NPM_BIN=npm ./scripts/check_env.sh
```
