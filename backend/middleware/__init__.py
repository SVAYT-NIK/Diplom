"""
Middleware module for authentication, authorization, logging, and request/response processing.
Implements JWT validation, RBAC checks, CORS, and audit logging.
"""

from backend.middleware.auth import JWTAuthMiddleware, get_current_user
from backend.middleware.logging import AuditLogMiddleware

__all__ = ["JWTAuthMiddleware", "get_current_user", "AuditLogMiddleware"]