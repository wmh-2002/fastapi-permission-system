from typing import Generic, TypeVar, Optional, Union
from pydantic import BaseModel
from fastapi import status
from fastapi.responses import JSONResponse

T = TypeVar('T')

class APIResponse(BaseModel, Generic[T]):
    """
    统一的 API 响应模板
    """
    success: bool
    code: int
    message: str
    data: Optional[T] = None
    error: Optional[str] = None

    class Config:
        from_attributes = True

def success_response(data: T = None, message: str = "成功", code: int = status.HTTP_200_OK) -> APIResponse[T]:
    """
    创建成功响应
    """
    return APIResponse(
        success=True,
        code=code,
        message=message,
        data=data
    )

def error_response(error: str = "发生错误", message: str = "错误", code: int = status.HTTP_400_BAD_REQUEST) -> APIResponse[None]:
    """
    创建错误响应
    """
    return APIResponse(
        success=False,
        code=code,
        message=message,
        error=error
    )

def create_json_response(response: APIResponse) -> JSONResponse:
    """
    从 APIResponse 创建 FastAPI JSONResponse
    """
    return JSONResponse(
        status_code=response.code,
        content=response.model_dump()
    )