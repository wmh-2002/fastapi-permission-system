from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.utils.security import verify_token
from backend.database.user_models import User
from typing import Optional, List
import jwt


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    从 JWT 令牌中获取当前认证用户
    """
    token = credentials.credentials
    payload = verify_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的身份验证凭据",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的身份验证凭据",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户未找到",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.status:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户账户已停用",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


def require_permission(permission_name: str):
    """
    依赖项，用于检查当前用户是否具有特定权限
    """
    def permission_checker(
        current_user: User = Depends(get_current_user)
    ) -> bool:
        # 从用户角色获取用户权限
        user_permissions = set()
        for role in current_user.roles:
            for perm in role.permissions:
                user_permissions.add(perm.name)
        
        # 检查用户是否具有所需权限
        if permission_name not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"需要权限 '{permission_name}'"
            )
        
        return True
    
    return permission_checker


def require_any_permission(permission_names: List[str]):
    """
    依赖项，用于检查当前用户是否具有指定权限中的至少一个
    """
    def permission_checker(
        current_user: User = Depends(get_current_user)
    ) -> bool:
        # 从用户角色获取用户权限
        user_permissions = set()
        for role in current_user.roles:
            for perm in role.permissions:
                user_permissions.add(perm.name)
        
        # 检查用户是否至少具有一个所需权限
        has_permission = any(perm in user_permissions for perm in permission_names)
        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"需要以下权限之一: {', '.join(permission_names)}"
            )
        
        return True
    
    return permission_checker


def require_role(role_name: str):
    """
    依赖项，用于检查当前用户是否具有特定角色
    """
    def role_checker(
        current_user: User = Depends(get_current_user)
    ) -> bool:
        # 检查用户是否具有所需角色
        user_roles = [role.name for role in current_user.roles]
        if role_name not in user_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"需要角色 '{role_name}'"
            )
        
        return True
    
    return role_checker