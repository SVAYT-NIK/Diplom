from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

from backend.core.security import verify_token, TokenData
from backend.core.config import get_settings

settings = get_settings()
security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> TokenData:
    """Получение текущего пользователя из JWT токена."""
    
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не предоставлены учётные данные",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = credentials.credentials
    token_data = verify_token(token, expected_type="access")
    
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный или истёкший токен",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return token_data


def require_role(*allowed_roles: str):
    """Декоратор для ограничения доступа по ролям."""
    
    async def role_checker(current_user: TokenData = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Требуется одна из ролей: {', '.join(allowed_roles)}",
            )
        return current_user
    
    return role_checker


def require_mcd_access(mcd_id_param: str = "mcd_id"):
    """Проверка доступа к конкретному МКД."""
    
    async def mcd_access_checker(
        mcd_id: str,
        current_user: TokenData = Depends(get_current_user)
    ):
        # Admin имеет доступ ко всем МКД
        if current_user.role == "admin":
            return current_user
        
        # Проверка наличия МКД в списке доступа
        if current_user.mcd_access is None or mcd_id not in current_user.mcd_access:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Нет доступа к МКД {mcd_id}",
            )
        
        return current_user
    
    return mcd_access_checker
