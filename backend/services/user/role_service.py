"""
角色相关操作的服务层
"""

from sqlalchemy.orm import Session
from backend.database.user_models import Role, Permission
from backend.schemas.user import RoleCreate, RoleUpdate
from typing import List, Optional


def get_role_by_id(db: Session, role_id: int) -> Optional[Role]:
    """
    根据ID获取角色
    """
    return db.query(Role).filter(Role.id == role_id).first()

def get_role_by_name(db: Session, name: str) -> Optional[Role]:
    """
    根据名称获取角色
    """
    return db.query(Role).filter(Role.name == name).first()

def get_roles(db: Session, skip: int = 0, limit: int = 100) -> List[Role]:
    """
    分页获取角色列表
    """
    return db.query(Role).offset(skip).limit(limit).all()

def create_role(db: Session, role_data: RoleCreate) -> Role:
    """
    创建新角色
    """
    # 检查角色名称是否已存在
    existing_role = db.query(Role).filter(Role.name == role_data.name).first()
    if existing_role:
        raise ValueError("角色名称已存在")
    
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
    更新角色
    """
    db_role = db.query(Role).filter(Role.id == role_id).first()
    if not db_role:
        return None
    
    # 检查新名称是否与现有角色冲突
    if role_update.name and role_update.name != db_role.name:
        existing_role = db.query(Role).filter(Role.name == role_update.name).first()
        if existing_role:
            raise ValueError("角色名称已存在")
    
    # 更新字段
    if role_update.name is not None:
        db_role.name = role_update.name
    if role_update.description is not None:
        db_role.description = role_update.description
    
    db.commit()
    db.refresh(db_role)
    return db_role

def delete_role(db: Session, role_id: int) -> bool:
    """
    删除角色
    """
    db_role = db.query(Role).filter(Role.id == role_id).first()
    if not db_role:
        return False
    
    db.delete(db_role)
    db.commit()
    return True

def add_permission_to_role(db: Session, role_id: int, permission_id: int) -> bool:
    """
    为角色添加权限
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
    从角色移除权限
    """
    role = db.query(Role).filter(Role.id == role_id).first()
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    
    if not role or not permission:
        return False
    
    if permission in role.permissions:
        role.permissions.remove(permission)
        db.commit()
    
    return True