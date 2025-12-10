from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.database.user_models import User, Permission, PermissionLog
from typing import Generator
import logging

logger = logging.getLogger(__name__)


class PermissionLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        
        # 如果用户已认证，则记录权限访问日志
        if "authorization" in request.headers:
            auth_header = request.headers["authorization"]
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
                
                # 从令牌中提取用户信息（此示例已简化）
                # 在实际实现中，你会解码 JWT 并获取用户 ID
                # 为简单起见，我们暂时跳过实际的日志记录
                pass
        
        return response