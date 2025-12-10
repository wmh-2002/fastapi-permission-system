from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas.user import UserCreate, UserResponse, Token
from backend.services.auth_service import authenticate_user, register_user, create_access_token_for_user
from backend.utils.responses import success_response, error_response, create_json_response

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    注册新用户
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
        response = success_response(data=user_response, message="用户注册成功")
        return create_json_response(response)
    except ValueError as e:
        response = error_response(error=str(e), message="注册失败", code=status.HTTP_400_BAD_REQUEST)
        return create_json_response(response)


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    登录端点，返回 JWT 令牌
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        response = error_response(error="用户名或密码错误", message="认证失败", code=status.HTTP_401_UNAUTHORIZED)
        return create_json_response(response)
    
    if not user.status:
        response = error_response(error="用户账户已停用", message="账户已停用", code=status.HTTP_401_UNAUTHORIZED)
        return create_json_response(response)
    
    access_token = create_access_token_for_user(user)
    token = Token(access_token=access_token, token_type="bearer")
    
    response = success_response(data=token, message="登录成功")
    return create_json_response(response)