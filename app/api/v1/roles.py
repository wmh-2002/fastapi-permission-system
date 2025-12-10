from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import RoleCreate, RoleUpdate, RoleResponse
from app.services.role_service import (
    get_role_by_id, get_role_by_name, get_roles, create_role, 
    update_role, delete_role, add_permission_to_role, remove_permission_from_role
)
from app.utils.responses import success_response, error_response, create_json_response
from app.api.deps import require_permission, get_current_user
from app.database.models import User
from app.constants.permissions import PERMISSIONS

router = APIRouter()


@router.get("/", response_model=dict)
async def list_roles(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a list of roles with pagination
    Requires: role:read permission
    """
    # Check if user has permission to read roles
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
    
    response = success_response(data={"roles": roles_response, "total": len(roles_response)}, message="Roles retrieved successfully")
    return create_json_response(response)


@router.get("/{role_id}", response_model=RoleResponse)
async def get_role(
    role_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a role by ID
    Requires: role:read permission
    """
    # Check if user has permission to read roles
    require_permission(PERMISSIONS["ROLE_READ"])(current_user)
    
    db_role = get_role_by_id(db, role_id)
    if not db_role:
        response = error_response(error="Role not found", message="Role not found", code=status.HTTP_404_NOT_FOUND)
        return create_json_response(response)
    
    role_response = RoleResponse(
        id=db_role.id,
        name=db_role.name,
        description=db_role.description,
        created_at=db_role.created_at,
        updated_at=db_role.updated_at,
        permissions=[perm.name for perm in db_role.permissions]
    )
    
    response = success_response(data=role_response, message="Role retrieved successfully")
    return create_json_response(response)


@router.post("/", response_model=RoleResponse)
async def create_new_role(
    role_data: RoleCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new role
    Requires: role:create permission
    """
    # Check if user has permission to create roles
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
        response = success_response(data=role_response, message="Role created successfully")
        return create_json_response(response)
    except ValueError as e:
        response = error_response(error=str(e), message="Role creation failed", code=status.HTTP_400_BAD_REQUEST)
        return create_json_response(response)


@router.put("/{role_id}", response_model=RoleResponse)
async def update_existing_role(
    role_id: int, 
    role_update: RoleUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a role
    Requires: role:update permission
    """
    # Check if user has permission to update roles
    require_permission(PERMISSIONS["ROLE_UPDATE"])(current_user)
    
    try:
        db_role = update_role(db, role_id, role_update)
        if not db_role:
            response = error_response(error="Role not found", message="Role not found", code=status.HTTP_404_NOT_FOUND)
            return create_json_response(response)
        
        role_response = RoleResponse(
            id=db_role.id,
            name=db_role.name,
            description=db_role.description,
            created_at=db_role.created_at,
            updated_at=db_role.updated_at,
            permissions=[perm.name for perm in db_role.permissions]
        )
        response = success_response(data=role_response, message="Role updated successfully")
        return create_json_response(response)
    except ValueError as e:
        response = error_response(error=str(e), message="Role update failed", code=status.HTTP_400_BAD_REQUEST)
        return create_json_response(response)


@router.delete("/{role_id}")
async def delete_existing_role(
    role_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a role
    Requires: role:delete permission
    """
    # Check if user has permission to delete roles
    require_permission(PERMISSIONS["ROLE_DELETE"])(current_user)
    
    success = delete_role(db, role_id)
    if not success:
        response = error_response(error="Role not found", message="Role not found", code=status.HTTP_404_NOT_FOUND)
        return create_json_response(response)
    
    response = success_response(message="Role deleted successfully")
    return create_json_response(response)


@router.post("/{role_id}/permissions/{permission_id}")
async def add_permission_to_role_endpoint(
    role_id: int, 
    permission_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Add a permission to a role
    Requires: role:update permission
    """
    # Check if user has permission to update roles
    require_permission(PERMISSIONS["ROLE_UPDATE"])(current_user)
    
    success = add_permission_to_role(db, role_id, permission_id)
    if not success:
        response = error_response(error="Role or permission not found", message="Assignment failed", code=status.HTTP_404_NOT_FOUND)
        return create_json_response(response)
    
    response = success_response(message="Permission added to role successfully")
    return create_json_response(response)


@router.delete("/{role_id}/permissions/{permission_id}")
async def remove_permission_from_role_endpoint(
    role_id: int, 
    permission_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Remove a permission from a role
    Requires: role:update permission
    """
    # Check if user has permission to update roles
    require_permission(PERMISSIONS["ROLE_UPDATE"])(current_user)
    
    success = remove_permission_from_role(db, role_id, permission_id)
    if not success:
        response = error_response(error="Role or permission not found", message="Removal failed", code=status.HTTP_404_NOT_FOUND)
        return create_json_response(response)
    
    response = success_response(message="Permission removed from role successfully")
    return create_json_response(response)