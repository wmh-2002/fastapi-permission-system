"""
Service layer for role-related operations
"""

from sqlalchemy.orm import Session
from app.database.models import Role, Permission
from app.schemas.user import RoleCreate, RoleUpdate
from typing import List, Optional


def get_role_by_id(db: Session, role_id: int) -> Optional[Role]:
    """
    Retrieve a role by ID
    """
    return db.query(Role).filter(Role.id == role_id).first()


def get_role_by_name(db: Session, name: str) -> Optional[Role]:
    """
    Retrieve a role by name
    """
    return db.query(Role).filter(Role.name == name).first()


def get_roles(db: Session, skip: int = 0, limit: int = 100) -> List[Role]:
    """
    Retrieve a list of roles with pagination
    """
    return db.query(Role).offset(skip).limit(limit).all()


def create_role(db: Session, role_data: RoleCreate) -> Role:
    """
    Create a new role
    """
    # Check if role name already exists
    existing_role = db.query(Role).filter(Role.name == role_data.name).first()
    if existing_role:
        raise ValueError("Role name already exists")
    
    db_role = Role(
        name=role_data.name,
        description=role_data.description
    )
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


def update_role(db: Session, role_id: int, role_update: RoleUpdate) -> Optional[Role]:
    """
    Update a role
    """
    db_role = db.query(Role).filter(Role.id == role_id).first()
    if not db_role:
        return None
    
    # Check if new name conflicts with existing roles
    if role_update.name and role_update.name != db_role.name:
        existing_role = db.query(Role).filter(Role.name == role_update.name).first()
        if existing_role:
            raise ValueError("Role name already exists")
    
    # Update fields
    if role_update.name is not None:
        db_role.name = role_update.name
    if role_update.description is not None:
        db_role.description = role_update.description
    
    db.commit()
    db.refresh(db_role)
    return db_role


def delete_role(db: Session, role_id: int) -> bool:
    """
    Delete a role
    """
    db_role = db.query(Role).filter(Role.id == role_id).first()
    if not db_role:
        return False
    
    db.delete(db_role)
    db.commit()
    return True


def add_permission_to_role(db: Session, role_id: int, permission_id: int) -> bool:
    """
    Add a permission to a role
    """
    role = db.query(Role).filter(Role.id == role_id).first()
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    
    if not role or not permission:
        return False
    
    if permission not in role.permissions:
        role.permissions.append(permission)
        db.commit()
    
    return True


def remove_permission_from_role(db: Session, role_id: int, permission_id: int) -> bool:
    """
    Remove a permission from a role
    """
    role = db.query(Role).filter(Role.id == role_id).first()
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    
    if not role or not permission:
        return False
    
    if permission in role.permissions:
        role.permissions.remove(permission)
        db.commit()
    
    return True