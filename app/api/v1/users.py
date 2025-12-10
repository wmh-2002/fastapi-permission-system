from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services.user_service import (
    get_user_by_id, get_user_by_username, get_users, create_user, 
    update_user, delete_user, assign_role_to_user, remove_role_from_user
)
from app.utils.responses import success_response, error_response, create_json_response
from app.api.deps import require_permission, require_role, get_current_user
from app.database.models import User
from app.constants.permissions import PERMISSIONS

router = APIRouter()


@router.get("/", response_model=dict)
async def list_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a list of users with pagination
    Requires: user:read permission
    """
    # Check if user has permission to read users
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
    
    response = success_response(data={"users": users_response, "total": len(users_response)}, message="Users retrieved successfully")
    return create_json_response(response)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a user by ID
    Requires: user:read permission
    """
    # Check if user has permission to read users
    require_permission(PERMISSIONS["USER_READ"])(current_user)
    
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        response = error_response(error="User not found", message="User not found", code=status.HTTP_404_NOT_FOUND)
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
    
    response = success_response(data=user_response, message="User retrieved successfully")
    return create_json_response(response)


@router.post("/", response_model=UserResponse)
async def create_new_user(
    user_data: UserCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new user
    Requires: user:create permission
    """
    # Check if user has permission to create users
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
        response = success_response(data=user_response, message="User created successfully")
        return create_json_response(response)
    except ValueError as e:
        response = error_response(error=str(e), message="User creation failed", code=status.HTTP_400_BAD_REQUEST)
        return create_json_response(response)


@router.put("/{user_id}", response_model=UserResponse)
async def update_existing_user(
    user_id: int, 
    user_update: UserUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a user
    Requires: user:update permission
    """
    # Check if user has permission to update users
    require_permission(PERMISSIONS["USER_UPDATE"])(current_user)
    
    try:
        db_user = update_user(db, user_id, user_update)
        if not db_user:
            response = error_response(error="User not found", message="User not found", code=status.HTTP_404_NOT_FOUND)
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
        response = success_response(data=user_response, message="User updated successfully")
        return create_json_response(response)
    except ValueError as e:
        response = error_response(error=str(e), message="User update failed", code=status.HTTP_400_BAD_REQUEST)
        return create_json_response(response)


@router.delete("/{user_id}")
async def delete_existing_user(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a user
    Requires: user:delete permission
    """
    # Check if user has permission to delete users
    require_permission(PERMISSIONS["USER_DELETE"])(current_user)
    
    success = delete_user(db, user_id)
    if not success:
        response = error_response(error="User not found", message="User not found", code=status.HTTP_404_NOT_FOUND)
        return create_json_response(response)
    
    response = success_response(message="User deleted successfully")
    return create_json_response(response)


@router.post("/{user_id}/roles/{role_id}")
async def assign_role_to_user_endpoint(
    user_id: int, 
    role_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Assign a role to a user
    Requires: user:update permission
    """
    # Check if user has permission to update users
    require_permission(PERMISSIONS["USER_UPDATE"])(current_user)
    
    success = assign_role_to_user(db, user_id, role_id)
    if not success:
        response = error_response(error="User or role not found", message="Assignment failed", code=status.HTTP_404_NOT_FOUND)
        return create_json_response(response)
    
    response = success_response(message="Role assigned successfully")
    return create_json_response(response)


@router.delete("/{user_id}/roles/{role_id}")
async def remove_role_from_user_endpoint(
    user_id: int, 
    role_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Remove a role from a user
    Requires: user:update permission
    """
    # Check if user has permission to update users
    require_permission(PERMISSIONS["USER_UPDATE"])(current_user)
    
    success = remove_role_from_user(db, user_id, role_id)
    if not success:
        response = error_response(error="User or role not found", message="Removal failed", code=status.HTTP_404_NOT_FOUND)
        return create_json_response(response)
    
    response = success_response(message="Role removed successfully")
    return create_json_response(response)