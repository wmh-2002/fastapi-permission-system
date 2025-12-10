from typing import Generic, TypeVar, Optional, Union
from pydantic import BaseModel
from fastapi import status
from fastapi.responses import JSONResponse

T = TypeVar('T')

class APIResponse(BaseModel, Generic[T]):
    """
    Unified API response template
    """
    success: bool
    code: int
    message: str
    data: Optional[T] = None
    error: Optional[str] = None

    class Config:
        from_attributes = True

def success_response(data: T = None, message: str = "Success", code: int = status.HTTP_200_OK) -> APIResponse[T]:
    """
    Create a success response
    """
    return APIResponse(
        success=True,
        code=code,
        message=message,
        data=data
    )

def error_response(error: str = "An error occurred", message: str = "Error", code: int = status.HTTP_400_BAD_REQUEST) -> APIResponse[None]:
    """
    Create an error response
    """
    return APIResponse(
        success=False,
        code=code,
        message=message,
        error=error
    )

def create_json_response(response: APIResponse) -> JSONResponse:
    """
    Create a FastAPI JSONResponse from APIResponse
    """
    return JSONResponse(
        status_code=response.code,
        content=response.model_dump()
    )