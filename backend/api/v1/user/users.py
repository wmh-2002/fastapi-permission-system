from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas.user import UserCreate, UserUpdate, UserResponse
from backend.services.user_service import (
    get_user_by_id, get_user_by_username, get_users, create_user, 
    update_user, delete_user, assign_role_to_user, remove_role_from_user
)
from backend.utils.responses import success_response, error_response, create_json_response
from backend.api.deps import require_permission, require_role, get_current_user
from backend.database.user_models import User
from backend.constants.permissions import PERMISSIONS

router = APIRouter()


@router.get("/", response_model=dict)
async def list_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    分页获取用户列表
    需要: user:read 权限
    """
    # 检查用户是否有读取用户的权限
    require_permission(PERMISSIONS["USER_READ"])(current_user)
    
    db_users = get_users(db, skip=skip, limit=limit)
    users_response = []
    
    for user in db_users:
        user_response = UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            created_at=user.created_at,
            updated_at=user.updated_at,
            status=user.status,
            roles=[role.name for role in user.roles]
        )
        users_response.append(user_response)
    
    response = success_response(data={"users": users_response, "total": len(users_response)}, message="用户获取成功")
    return create_json_response(response)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    根据ID获取用户
    需要: user:read 权限
    """
    # 检查用户是否有读取用户的权限
    require_permission(PERMISSIONS["USER_READ"])(current_user)
    
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        response = error_response(error="用户未找到", message="用户未找到", code=status.HTTP_404_NOT_FOUND)
        return create_json_response(response)
    
    user_response = UserResponse(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        created_at=db_user.created_at,
        updated_at=db_user.updated_at,
        status=db_user.status,
        roles=[role.name for role in db_user.roles]
    )
    
    response = success_response(data=user_response, message="用户获取成功")
    return create_json_response(response)


@router.post("/", response_model=UserResponse)
async def create_new_user(
    user_data: UserCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建新用户
    需要: user:create 权限
    """
    # 检查用户是否有创建用户的权限
    require_permission(PERMISSIONS["USER_CREATE"])(current_user)
    
    try:
        db_user = create_user(db, user_data)
        user_response = UserResponse(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at,
            status=db_user.status,
            roles=[role.name for role in db_user.roles]
        )
        response = success_response(data=user_response, message="用户创建成功")
        return create_json_response(response)
    except ValueError as e:
        response = error_response(error=str(e), message="用户创建失败", code=status.HTTP_400_BAD_REQUEST)
        return create_json_response(response)


@router.put("/{user_id}", response_model=UserResponse)
async def update_existing_user(
    user_id: int, 
    user_update: UserUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    更新用户
    需要: user:update 权限
    """
    # 检查用户是否有更新用户的权限
    require_permission(PERMISSIONS["USER_UPDATE"])(current_user)
    
    try:
        db_user = update_user(db, user_id, user_update)
        if not db_user:
            response = error_response(error="用户未找到", message="用户未找到", code=status.HTTP_404_NOT_FOUND)
            return create_json_response(response)
        
        user_response = UserResponse(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at,
            status=db_user.status,
            roles=[role.name for role in db_user.roles]
        )
        response = success_response(data=user_response, message="用户更新成功")
        return create_json_response(response)
    except ValueError as e:
        response = error_response(error=str(e), message="用户更新失败", code=status.HTTP_400_BAD_REQUEST)
        return create_json_response(response)


@router.delete("/{user_id}")
async def delete_existing_user(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    删除用户
    需要: user:delete 权限
    """
    # 检查用户是否有删除用户的权限
    require_permission(PERMISSIONS["USER_DELETE"])(current_user)
    
    success = delete_user(db, user_id)
    if not success:
        response = error_response(error="用户未找到", message="用户未找到", code=status.HTTP_404_NOT_FOUND)
        return create_json_response(response)
    
    response = success_response(message="用户删除成功")
    return create_json_response(response)


@router.post("/{user_id}/roles/{role_id}")
async def assign_role_to_user_endpoint(
    user_id: int, 
    role_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    为用户分配角色
    需要: user:update 权限
    """
    # 检查用户是否有更新用户的权限
    require_permission(PERMISSIONS["USER_UPDATE"])(current_user)
    
    success = assign_role_to_user(db, user_id, role_id)
    if not success:
        response = error_response(error="用户或角色未找到", message="分配失败", code=status.HTTP_404_NOT_FOUND)
        return create_json_response(response)
    
    response = success_response(message="角色分配成功")
    return create_json_response(response)


@router.delete("/{user_id}/roles/{role_id}")
async def remove_role_from_user_endpoint(
    user_id: int, 
    role_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    从用户移除角色
    需要: user:update 权限
    """
    # 检查用户是否有更新用户的权限
    require_permission(PERMISSIONS["USER_UPDATE"])(current_user)
    
    success = remove_role_from_user(db, user_id, role_id)
    if not success:
        response = error_response(error="用户或角色未找到", message="移除失败", code=status.HTTP_404_NOT_FOUND)
        return create_json_response(response)
    
    response = success_response(message="角色移除成功")
    return create_json_response(response)