from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from sqlalchemy.orm import Session
from app.database import get_db
from app.database.models import User, Permission, PermissionLog
from typing import Generator
import logging

logger = logging.getLogger(__name__)


class PermissionLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        
        # Log permission access if user is authenticated
        if "authorization" in request.headers:
            auth_header = request.headers["authorization"]
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
                
                # Extract user information from token (simplified for this example)
                # In a real implementation, you'd decode the JWT and get the user ID
                # For now, we'll skip the actual logging to keep it simple
                pass
        
        return response