from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import structlog
from contextlib import asynccontextmanager

from backend.core.config import get_settings
from backend.db.session import init_db, close_db

settings = get_settings()
logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения."""
    # Startup
    logger.info("application_startup", version=settings.app_version)
    await init_db()
    yield
    # Shutdown
    await close_db()
    logger.info("application_shutdown")


def create_app() -> FastAPI:
    """Фабрика приложения FastAPI."""
    
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Система анализа энергоэффективности МКД",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Request logging middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        import time
        start_time = time.time()
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        logger.info(
            "request_processed",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            process_time_ms=round(process_time * 1000, 2),
        )
        
        response.headers["X-Process-Time"] = str(round(process_time * 1000, 2))
        return response
    
    # Exception handlers
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.warning("validation_error", errors=exc.errors())
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "code": "VALIDATION_ERROR",
                "message": "Ошибка валидации данных",
                "details": exc.errors(),
            },
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error("unhandled_exception", error=str(exc), path=request.url.path)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "code": "INTERNAL_ERROR",
                "message": "Внутренняя ошибка сервера",
            },
        )
    
    # Include routers
    from backend.api.endpoints import auth, ingest, analytics, forecast, anomalies, reports, compliance, admin
    
    app.include_router(auth.router, prefix=f"{settings.api_prefix}/auth", tags=["Auth"])
    app.include_router(ingest.router, prefix=f"{settings.api_prefix}/ingest", tags=["Ingest"])
    app.include_router(analytics.router, prefix=f"{settings.api_prefix}/analytics", tags=["Analytics"])
    app.include_router(forecast.router, prefix=f"{settings.api_prefix}/forecast", tags=["Forecast"])
    app.include_router(anomalies.router, prefix=f"{settings.api_prefix}/anomalies", tags=["Anomalies"])
    app.include_router(reports.router, prefix=f"{settings.api_prefix}/reports", tags=["Reports"])
    app.include_router(compliance.router, prefix=f"{settings.api_prefix}/compliance", tags=["Compliance"])
    app.include_router(admin.router, prefix=f"{settings.api_prefix}/admin", tags=["Admin"])
    
    # Health checks (no auth required)
    @app.get("/health", tags=["System"])
    async def health_check():
        return {"status": "healthy", "version": settings.app_version}
    
    @app.get("/health/ready", tags=["System"])
    async def readiness_check():
        # TODO: Check DB, cache, broker connections
        return {"status": "ready"}
    
    return app
