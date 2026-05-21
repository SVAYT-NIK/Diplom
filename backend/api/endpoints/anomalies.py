"""
Anomaly detection endpoints.
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

router = APIRouter()


class AnomalyResponse(BaseModel):
    mcd_id: str
    anomalies: List[dict]
    detection_method: str
    period: dict


@router.get("/{mcd_id}", response_model=AnomalyResponse)
async def get_anomalies(
    mcd_id: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    method: Optional[str] = "consensus"
):
    """Получение обнаруженных аномалий."""
    # TODO: Implement anomaly detection
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Anomaly detection not implemented yet"
    )


@router.post("/detect")
async def detect_anomalies(mcd_id: str, data: List[dict]):
    """Запуск детекции аномалий на новых данных."""
    # TODO: Implement real-time anomaly detection
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Real-time anomaly detection not implemented yet"
    )
