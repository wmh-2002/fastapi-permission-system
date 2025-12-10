from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import users, roles, permissions, auth
from app.config import settings

app = FastAPI(
    title="FastAPI Permission Management System",
    description="A comprehensive permission management system built with FastAPI",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(auth.router, prefix="/api/v1", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1", tags=["Users"])
app.include_router(roles.router, prefix="/api/v1", tags=["Roles"])
app.include_router(permissions.router, prefix="/api/v1", tags=["Permissions"])

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Permission Management System"}