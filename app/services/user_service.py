"""
Service layer for user-related operations
"""

from sqlalchemy.orm import Session
from app.database.models import User, Role
from app.schemas.user import UserCreate, UserUpdate, UserInDB
from app.utils.security import get_password_hash
from typing import List, Optional


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """
    Retrieve a user by ID
    """
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """
    Retrieve a user by username
    """
    return db.query(User).filter(User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """
    Retrieve a list of users with pagination
    """
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user_data: UserCreate) -> User:
    """
    Create a new user
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


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    """
    Update a user
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None
    
    # Check if new username conflicts with existing users
    if user_update.username and user_update.username != db_user.username:
        existing_user = db.query(User).filter(User.username == user_update.username).first()
        if existing_user:
            raise ValueError("Username already exists")
    
    # Check if new email conflicts with existing users
    if user_update.email and user_update.email != db_user.email:
        existing_email = db.query(User).filter(User.email == user_update.email).first()
        if existing_email:
            raise ValueError("Email already exists")
    
    # Update fields
    if user_update.username is not None:
        db_user.username = user_update.username
    if user_update.email is not None:
        db_user.email = user_update.email
    if user_update.status is not None:
        db_user.status = user_update.status
    if user_update.password is not None:
        db_user.password = get_password_hash(user_update.password)
    
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    """
    Delete a user
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True


def assign_role_to_user(db: Session, user_id: int, role_id: int) -> bool:
    """
    Assign a role to a user
    """
    user = db.query(User).filter(User.id == user_id).first()
    role = db.query(Role).filter(Role.id == role_id).first()
    
    if not user or not role:
        return False
    
    if role not in user.roles:
        user.roles.append(role)
        db.commit()
    
    return True


def remove_role_from_user(db: Session, user_id: int, role_id: int) -> bool:
    """
    Remove a role from a user
    """
    user = db.query(User).filter(User.id == user_id).first()
    role = db.query(Role).filter(Role.id == role_id).first()
    
    if not user or not role:
        return False
    
    if role in user.roles:
        user.roles.remove(role)
        db.commit()
    
    return True