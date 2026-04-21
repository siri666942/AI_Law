
import sys
import os

print(f"Python version: {sys.version}")
print(f"Python path: {sys.path}")

# 检查site-packages目录
try:
    import site
    user_site = site.getusersitepackages()
    print(f"User site packages: {user_site}")
    print(f"User site packages in PATH: {user_site in sys.path}")
except Exception as e:
    print(f"Error: {e}")

# 尝试导入uvicorn
try:
    import uvicorn
    print("uvicorn is installed")
except ImportError:
    print("uvicorn is NOT installed")

# 尝试导入fastapi
try:
    import fastapi
    print("fastapi is installed")
except ImportError:
    print("fastapi is NOT installed")
