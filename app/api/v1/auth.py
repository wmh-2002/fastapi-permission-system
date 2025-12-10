from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserResponse, Token
from app.services.auth_service import authenticate_user, register_user, create_access_token_for_user
from app.utils.responses import success_response, error_response, create_json_response

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user
    """
    try:
        db_user = register_user(db, user_data)
        user_response = UserResponse(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at,
            status=db_user.status,
            roles=[role.name for role in db_user.roles]
        )
        response = success_response(data=user_response, message="User registered successfully")
        return create_json_response(response)
    except ValueError as e:
        response = error_response(error=str(e), message="Registration failed", code=status.HTTP_400_BAD_REQUEST)
        return create_json_response(response)


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Login endpoint that returns a JWT token
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        response = error_response(error="Incorrect username or password", message="Authentication failed", code=status.HTTP_401_UNAUTHORIZED)
        return create_json_response(response)
    
    if not user.status:
        response = error_response(error="User account is deactivated", message="Account deactivated", code=status.HTTP_401_UNAUTHORIZED)
        return create_json_response(response)
    
    access_token = create_access_token_for_user(user)
    token = Token(access_token=access_token, token_type="bearer")
    
    response = success_response(data=token, message="Login successful")
    return create_json_response(response)