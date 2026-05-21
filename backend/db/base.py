"""Base class for SQLAlchemy models."""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Базовый класс для всех ORM моделей.
    
    Используется как основа для декларативного определения моделей
    в SQLAlchemy 2.0+ стиле.
    """
    pass
