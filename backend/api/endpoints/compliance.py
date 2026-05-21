"""
Compliance endpoints for regulatory compliance checks (PP RF 354, etc.).
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter()


class ComplianceResponse(BaseModel):
    mcd_id: str
    status: str  # Эффективный, Нормативный, Критический
    eta: float
    deviations: list
    period: dict


@router.get("/{mcd_id}/status")
async def get_compliance_status(
    mcd_id: str,
    period_start: Optional[datetime] = None,
    period_end: Optional[datetime] = None
):
    """Получение статуса соответствия нормативам."""
    # TODO: Implement compliance check
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Compliance check not implemented yet"
    )


@router.get("/{mcd_id}/deviations")
async def get_deviations(mcd_id: str):
    """Получение отклонений от нормативов."""
    # TODO: Implement deviations retrieval
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Deviations retrieval not implemented yet"
    )
