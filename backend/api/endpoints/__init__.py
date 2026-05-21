"""
API endpoints (routers) for FastAPI application.
Organized by domain: auth, metering, analytics, reports, admin.
"""

from backend.api.endpoints import auth, ingest, analytics, forecast, anomalies, reports, compliance, admin

__all__ = [
    "auth",
    "ingest",
    "analytics",
    "forecast",
    "anomalies",
    "reports",
    "compliance",
    "admin",
]