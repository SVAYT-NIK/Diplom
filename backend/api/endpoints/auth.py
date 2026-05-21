"""
Auth endpoints for user authentication and token management.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import Optional

router = APIRouter()


class TokenRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None


@router.post("/login", response_model=TokenResponse)
async def login(request: TokenRequest):
    """Получение JWT токена."""
    # TODO: Implement actual authentication
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Authentication not implemented yet"
    )


@router.post("/register", response_model=dict)
async def register(user: UserCreate):
    """Регистрация нового пользователя."""
    # TODO: Implement registration
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Registration not implemented yet"
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_token: str):
    """Обновление access токена."""
    # TODO: Implement token refresh
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Token refresh not implemented yet"
    )
