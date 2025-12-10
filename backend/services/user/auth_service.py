"""
认证相关操作的服务层
"""

from sqlalchemy.orm import Session
from backend.database.user_models import User
from backend.schemas.user import UserCreate, UserLogin
from backend.utils.security import verify_password, get_password_hash, create_access_token
from datetime import timedelta
from typing import Optional
from backend.config import settings
def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """
    通过用户名和密码验证用户
    """
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password):
        return None
    return user

def register_user(db: Session, user_data: UserCreate) -> User:
    """
    注册新用户
    """
    # 检查用户名是否已存在
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise ValueError("用户名已存在")
    
    # 检查邮箱是否已存在
    if user_data.email:
        existing_email = db.query(User).filter(User.email == user_data.email).first()
        if existing_email:
            raise ValueError("邮箱已存在")
    
    # 创建新用户
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        password=hashed_password,
        status=user_data.status
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_access_token_for_user(user: User) -> str:
    """
    为用户创建访问令牌
    """
    # 从角色获取用户权限
    permissions = []
    for role in user.roles:
        for perm in role.permissions:
            permissions.append(perm.name)
    
    data = {
        "sub": user.username,
        "permissions": permissions,
        "user_id": user.id
    }
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_access_token(data=data, expires_delta=access_token_expires)