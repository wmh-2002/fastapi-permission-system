from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas.user import PermissionCreate, PermissionUpdate, PermissionInDB
from backend.services.permission_service import (
    get_permission_by_id, get_permission_by_name, get_permissions, 
    create_permission, update_permission, delete_permission
)
from backend.utils.responses import success_response, error_response, create_json_response
from backend.api.deps import require_permission, get_current_user
from backend.database.user_models import User
from backend.constants.permissions import PERMISSIONS

router = APIRouter()


@router.get("/", response_model=dict)
async def list_permissions(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    分页获取权限列表
    需要: permission:read 权限
    """
    # 检查用户是否有读取权限的权限
    require_permission(PERMISSIONS["PERMISSION_READ"])(current_user)
    
    db_permissions = get_permissions(db, skip=skip, limit=limit)
    permissions_response = []
    
    for permission in db_permissions:
        permission_response = PermissionInDB(
            id=permission.id,
            name=permission.name,
            description=permission.description,
            created_at=permission.created_at,
            updated_at=permission.updated_at
        )
        permissions_response.append(permission_response)
    
    response = success_response(data={"permissions": permissions_response, "total": len(permissions_response)}, message="权限获取成功")
    return create_json_response(response)


@router.get("/{permission_id}", response_model=PermissionInDB)
async def get_permission(
    permission_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    根据ID获取权限
    需要: permission:read 权限
    """
    # 检查用户是否有读取权限的权限
    require_permission(PERMISSIONS["PERMISSION_READ"])(current_user)
    
    db_permission = get_permission_by_id(db, permission_id)
    if not db_permission:
        response = error_response(error="权限未找到", message="权限未找到", code=status.HTTP_404_NOT_FOUND)
        return create_json_response(response)
    
    permission_response = PermissionInDB(
        id=db_permission.id,
        name=db_permission.name,
        description=db_permission.description,
        created_at=db_permission.created_at,
        updated_at=db_permission.updated_at
    )
    
    response = success_response(data=permission_response, message="权限获取成功")
    return create_json_response(response)


@router.post("/", response_model=PermissionInDB)
async def create_new_permission(
    permission_data: PermissionCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建新权限
    需要: permission:create 权限
    """
    # 检查用户是否有创建权限的权限
    require_permission(PERMISSIONS["PERMISSION_CREATE"])(current_user)
    
    try:
        db_permission = create_permission(db, permission_data)
        permission_response = PermissionInDB(
            id=db_permission.id,
            name=db_permission.name,
            description=db_permission.description,
            created_at=db_permission.created_at,
            updated_at=db_permission.updated_at
        )
        response = success_response(data=permission_response, message="权限创建成功")
        return create_json_response(response)
    except ValueError as e:
        response = error_response(error=str(e), message="权限创建失败", code=status.HTTP_400_BAD_REQUEST)
        return create_json_response(response)


@router.put("/{permission_id}", response_model=PermissionInDB)
async def update_existing_permission(
    permission_id: int, 
    permission_update: PermissionUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    更新权限
    需要: permission:update 权限
    """
    # 检查用户是否有更新权限的权限
    require_permission(PERMISSIONS["PERMISSION_UPDATE"])(current_user)
    
    try:
        db_permission = update_permission(db, permission_id, permission_update)
        if not db_permission:
            response = error_response(error="权限未找到", message="权限未找到", code=status.HTTP_404_NOT_FOUND)
            return create_json_response(response)
        
        permission_response = PermissionInDB(
            id=db_permission.id,
            name=db_permission.name,
            description=db_permission.description,
            created_at=db_permission.created_at,
            updated_at=db_permission.updated_at
        )
        response = success_response(data=permission_response, message="权限更新成功")
        return create_json_response(response)
    except ValueError as e:
        response = error_response(error=str(e), message="权限更新失败", code=status.HTTP_400_BAD_REQUEST)
        return create_json_response(response)


@router.delete("/{permission_id}")
async def delete_existing_permission(
    permission_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    删除权限
    需要: permission:delete 权限
    """
    # 检查用户是否有删除权限的权限
    require_permission(PERMISSIONS["PERMISSION_DELETE"])(current_user)
    
    success = delete_permission(db, permission_id)
    if not success:
        response = error_response(error="权限未找到", message="权限未找到", code=status.HTTP_404_NOT_FOUND)
        return create_json_response(response)
    
    response = success_response(message="权限删除成功")
    return create_json_response(response)