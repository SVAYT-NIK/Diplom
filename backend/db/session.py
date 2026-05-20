from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from backend.core.config import get_settings

settings = get_settings()

# Engine для асинхронной работы с БД
engine = create_async_engine(
    settings.database_url,
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
    echo=settings.debug,
)

# Фабрика сессий
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Базовый класс для моделей
Base = declarative_base()


async def init_db():
    """Инициализация базы данных."""
    async with engine.begin() as conn:
        # Создание таблиц (в development режиме)
        if settings.debug:
            await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """Закрытие соединений с БД."""
    await engine.dispose()


async def get_db() -> AsyncSession:
    """Зависимость для получения сессии БД."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
