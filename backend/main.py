from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.v1.user import users, roles, permissions, auth
from backend.config import settings

app = FastAPI(
    title="FastAPI 权限管理系统",
    description="基于 FastAPI 构建的综合权限管理系统",
    version="1.0.0"
)

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含 API 路由
app.include_router(auth.router, prefix="/api/v1", tags=["认证"])
app.include_router(users.router, prefix="/api/v1", tags=["用户"])
app.include_router(roles.router, prefix="/api/v1", tags=["角色"])
app.include_router(permissions.router, prefix="/api/v1", tags=["权限"])

@app.get("/")
async def root():
    return {"message": "欢迎使用 FastAPI 权限管理系统"}