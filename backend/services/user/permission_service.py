"""
权限相关操作的服务层
"""

from sqlalchemy.orm import Session
from backend.database.user_models import Permission
from backend.schemas.user import PermissionCreate, PermissionUpdate
from typing import List, Optional


def get_permission_by_id(db: Session, permission_id: int) -> Optional[Permission]:
    """
    根据ID获取权限
    """
    return db.query(Permission).filter(Permission.id == permission_id).first()


def get_permission_by_name(db: Session, name: str) -> Optional[Permission]:
    """
    根据名称获取权限
    """
    return db.query(Permission).filter(Permission.name == name).first()


def get_permissions(db: Session, skip: int = 0, limit: int = 100) -> List[Permission]:
    """
    分页获取权限列表
    """
    return db.query(Permission).offset(skip).limit(limit).all()


def create_permission(db: Session, permission_data: PermissionCreate) -> Permission:
    """
    创建新权限
    """
    # 检查权限名称是否已存在
    existing_permission = db.query(Permission).filter(Permission.name == permission_data.name).first()
    if existing_permission:
        raise ValueError("权限名称已存在")
    
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
    更新权限
    """
    db_permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not db_permission:
        return None
    
    # 检查新名称是否与现有权限冲突
    if permission_update.name and permission_update.name != db_permission.name:
        existing_permission = db.query(Permission).filter(Permission.name == permission_update.name).first()
        if existing_permission:
            raise ValueError("权限名称已存在")
    
    # 更新字段
    if permission_update.name is not None:
        db_permission.name = permission_update.name
    if permission_update.description is not None:
        db_permission.description = permission_update.description
    
    db.commit()
    db.refresh(db_permission)
    return db_permission


def delete_permission(db: Session, permission_id: int) -> bool:
    """
    删除权限
    """
    db_permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not db_permission:
        return False
    
    db.delete(db_permission)
    db.commit()
    return True