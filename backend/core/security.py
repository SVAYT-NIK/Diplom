from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel

from backend.core.config import get_settings

settings = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TokenData(BaseModel):
    """Данные токена."""
    sub: str  # user id or username
    exp: datetime
    iat: datetime
    type: str  # access or refresh
    role: Optional[str] = None
    mcd_access: Optional[list[str]] = None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка пароля."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Хеширование пароля."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Создание JWT access токена."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.jwt_access_token_expire_minutes)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    })
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Создание JWT refresh токена."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=settings.jwt_refresh_token_expire_days)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh"
    })
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )
    return encoded_jwt


def decode_token(token: str) -> Optional[TokenData]:
    """Декодирование и валидация JWT токена."""
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )
        
        sub = payload.get("sub")
        exp = payload.get("exp")
        iat = payload.get("iat")
        token_type = payload.get("type")
        role = payload.get("role")
        mcd_access = payload.get("mcd_access", [])
        
        if sub is None or exp is None:
            return None
        
        return TokenData(
            sub=sub,
            exp=datetime.fromtimestamp(exp),
            iat=datetime.fromtimestamp(iat),
            type=token_type,
            role=role,
            mcd_access=mcd_access
        )
    except JWTError:
        return None


def verify_token(token: str, expected_type: str = "access") -> Optional[TokenData]:
    """Проверка токена на валидность и тип."""
    token_data = decode_token(token)
    
    if token_data is None:
        return None
    
    if token_data.type != expected_type:
        return None
    
    if datetime.utcnow() > token_data.exp:
        return None
    
    return token_data
