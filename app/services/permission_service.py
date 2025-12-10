"""
Service layer for permission-related operations
"""

from sqlalchemy.orm import Session
from app.database.models import Permission
from app.schemas.user import PermissionCreate, PermissionUpdate
from typing import List, Optional


def get_permission_by_id(db: Session, permission_id: int) -> Optional[Permission]:
    """
    Retrieve a permission by ID
    """
    return db.query(Permission).filter(Permission.id == permission_id).first()


def get_permission_by_name(db: Session, name: str) -> Optional[Permission]:
    """
    Retrieve a permission by name
    """
    return db.query(Permission).filter(Permission.name == name).first()


def get_permissions(db: Session, skip: int = 0, limit: int = 100) -> List[Permission]:
    """
    Retrieve a list of permissions with pagination
    """
    return db.query(Permission).offset(skip).limit(limit).all()


def create_permission(db: Session, permission_data: PermissionCreate) -> Permission:
    """
    Create a new permission
    """
    # Check if permission name already exists
    existing_permission = db.query(Permission).filter(Permission.name == permission_data.name).first()
    if existing_permission:
        raise ValueError("Permission name already exists")
    
    db_permission = Permission(
        name=permission_data.name,
        description=permission_data.description
    )
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission


def update_permission(db: Session, permission_id: int, permission_update: PermissionUpdate) -> Optional[Permission]:
    """
    Update a permission
    """
    db_permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not db_permission:
        return None
    
    # Check if new name conflicts with existing permissions
    if permission_update.name and permission_update.name != db_permission.name:
        existing_permission = db.query(Permission).filter(Permission.name == permission_update.name).first()
        if existing_permission:
            raise ValueError("Permission name already exists")
    
    # Update fields
    if permission_update.name is not None:
        db_permission.name = permission_update.name
    if permission_update.description is not None:
        db_permission.description = permission_update.description
    
    db.commit()
    db.refresh(db_permission)
    return db_permission


def delete_permission(db: Session, permission_id: int) -> bool:
    """
    Delete a permission
    """
    db_permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not db_permission:
        return False
    
    db.delete(db_permission)
    db.commit()
    return True