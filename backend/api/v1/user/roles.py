from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas.user import RoleCreate, RoleUpdate, RoleResponse
from backend.services.role_service import (
    get_role_by_id, get_role_by_name, get_roles, create_role, 
    update_role, delete_role, add_permission_to_role, remove_permission_from_role
)
from backend.utils.responses import success_response, error_response, create_json_response
from backend.api.deps import require_permission, get_current_user
from backend.database.user_models import User
from backend.constants.permissions import PERMISSIONS

router = APIRouter()


@router.get("/", response_model=dict)
async def list_roles(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    分页获取角色列表
    需要: role:read 权限
    """
    # 检查用户是否有读取角色的权限
    require_permission(PERMISSIONS["ROLE_READ"])(current_user)
    
    db_roles = get_roles(db, skip=skip, limit=limit)
    roles_response = []
    
    for role in db_roles:
        role_response = RoleResponse(
            id=role.id,
            name=role.name,
            description=role.description,
            created_at=role.created_at,
            updated_at=role.updated_at,
            permissions=[perm.name for perm in role.permissions]
        )
        roles_response.append(role_response)
    
    response = success_response(data={"roles": roles_response, "total": len(roles_response)}, message="角色获取成功")
    return create_json_response(response)


@router.get("/{role_id}", response_model=RoleResponse)
async def get_role(
    role_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    根据ID获取角色
    需要: role:read 权限
    """
    # 检查用户是否有读取角色的权限
    require_permission(PERMISSIONS["ROLE_READ"])(current_user)
    
    db_role = get_role_by_id(db, role_id)
    if not db_role:
        response = error_response(error="角色未找到", message="角色未找到", code=status.HTTP_404_NOT_FOUND)
        return create_json_response(response)
    
    role_response = RoleResponse(
        id=db_role.id,
        name=db_role.name,
        description=db_role.description,
        created_at=db_role.created_at,
        updated_at=db_role.updated_at,
        permissions=[perm.name for perm in db_role.permissions]
    )
    
    response = success_response(data=role_response, message="角色获取成功")
    return create_json_response(response)


@router.post("/", response_model=RoleResponse)
async def create_new_role(
    role_data: RoleCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建新角色
    需要: role:create 权限
    """
    # 检查用户是否有创建角色的权限
    require_permission(PERMISSIONS["ROLE_CREATE"])(current_user)
    
    try:
        db_role = create_role(db, role_data)
        role_response = RoleResponse(
            id=db_role.id,
            name=db_role.name,
            description=db_role.description,
            created_at=db_role.created_at,
            updated_at=db_role.updated_at,
            permissions=[perm.name for perm in db_role.permissions]
        )
        response = success_response(data=role_response, message="角色创建成功")
        return create_json_response(response)
    except ValueError as e:
        response = error_response(error=str(e), message="角色创建失败", code=status.HTTP_400_BAD_REQUEST)
        return create_json_response(response)


@router.put("/{role_id}", response_model=RoleResponse)
async def update_existing_role(
    role_id: int, 
    role_update: RoleUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    更新角色
    需要: role:update 权限
    """
    # 检查用户是否有更新角色的权限
    require_permission(PERMISSIONS["ROLE_UPDATE"])(current_user)
    
    try:
        db_role = update_role(db, role_id, role_update)
        if not db_role:
            response = error_response(error="角色未找到", message="角色未找到", code=status.HTTP_404_NOT_FOUND)
            return create_json_response(response)
        
        role_response = RoleResponse(
            id=db_role.id,
            name=db_role.name,
            description=db_role.description,
            created_at=db_role.created_at,
            updated_at=db_role.updated_at,
            permissions=[perm.name for perm in db_role.permissions]
        )
        response = success_response(data=role_response, message="角色更新成功")
        return create_json_response(response)
    except ValueError as e:
        response = error_response(error=str(e), message="角色更新失败", code=status.HTTP_400_BAD_REQUEST)
        return create_json_response(response)


@router.delete("/{role_id}")
async def delete_existing_role(
    role_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    删除角色
    需要: role:delete 权限
    """
    # 检查用户是否有删除角色的权限
    require_permission(PERMISSIONS["ROLE_DELETE"])(current_user)
    
    success = delete_role(db, role_id)
    if not success:
        response = error_response(error="角色未找到", message="角色未找到", code=status.HTTP_404_NOT_FOUND)
        return create_json_response(response)
    
    response = success_response(message="角色删除成功")
    return create_json_response(response)


@router.post("/{role_id}/permissions/{permission_id}")
async def add_permission_to_role_endpoint(
    role_id: int, 
    permission_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    为角色添加权限
    需要: role:update 权限
    """
    # 检查用户是否有更新角色的权限
    require_permission(PERMISSIONS["ROLE_UPDATE"])(current_user)
    
    success = add_permission_to_role(db, role_id, permission_id)
    if not success:
        response = error_response(error="角色或权限未找到", message="分配失败", code=status.HTTP_404_NOT_FOUND)
        return create_json_response(response)
    
    response = success_response(message="权限成功添加到角色")
    return create_json_response(response)


@router.delete("/{role_id}/permissions/{permission_id}")
async def remove_permission_from_role_endpoint(
    role_id: int, 
    permission_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    从角色移除权限
    需要: role:update 权限
    """
    # 检查用户是否有更新角色的权限
    require_permission(PERMISSIONS["ROLE_UPDATE"])(current_user)
    
    success = remove_permission_from_role(db, role_id, permission_id)
    if not success:
        response = error_response(error="角色或权限未找到", message="移除失败", code=status.HTTP_404_NOT_FOUND)
        return create_json_response(response)
    
    response = success_response(message="权限已成功从角色移除")
    return create_json_response(response)