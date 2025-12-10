"""
Service layer for authentication-related operations
"""

from sqlalchemy.orm import Session
from app.database.models import User
from app.schemas.user import UserCreate, UserLogin
from app.utils.security import verify_password, get_password_hash, create_access_token
from datetime import timedelta
from typing import Optional
from app.config import settings

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """
    Authenticate a user by username and password
    """
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password):
        return None
    return user


def register_user(db: Session, user_data: UserCreate) -> User:
    """
    Register a new user
    """
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise ValueError("Username already exists")
    
    # Check if email already exists
    if user_data.email:
        existing_email = db.query(User).filter(User.email == user_data.email).first()
        if existing_email:
            raise ValueError("Email already exists")
    
    # Create new user
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
    Create an access token for a user
    """
    # Get user permissions from roles
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