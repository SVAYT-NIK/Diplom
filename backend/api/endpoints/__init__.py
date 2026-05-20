"""
API endpoints (routers) for FastAPI application.
Organized by domain: auth, metering, analytics, reports, admin.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1")

# Import and include routers here when implemented
# from backend.api.endpoints import auth, metering, analytics, reports, admin
# router.include_router(auth.router, prefix="/auth", tags=["auth"])
# router.include_router(metering.router, prefix="/metering", tags=["metering"])
# router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
# router.include_router(reports.router, prefix="/reports", tags=["reports"])
# router.include_router(admin.router, prefix="/admin", tags=["admin"])

__all__ = ["router"]