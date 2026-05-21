"""
Middleware module for authentication, authorization, logging, and request/response processing.
Implements JWT validation, RBAC checks, CORS, and audit logging.
"""

from backend.middleware.auth import get_current_user, require_role, require_mcd_access

# Simple middleware wrapper for Starlette/FastAPI
class JWTAuthMiddleware:
    """JWT Authentication middleware wrapper."""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        # Middleware logic handled by FastAPI dependencies
        return await self.app(scope, receive, send)


__all__ = ["JWTAuthMiddleware", "get_current_user", "require_role", "require_mcd_access"]