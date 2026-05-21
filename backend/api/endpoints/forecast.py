"""
Forecast endpoints for energy consumption prediction.
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter()


class ForecastRequest(BaseModel):
    mcd_id: str
    horizon_hours: int = 24
    model_type: Optional[str] = "auto"


class ForecastResponse(BaseModel):
    mcd_id: str
    predictions: List[dict]
    model_used: str
    confidence_interval: dict


@router.post("/", response_model=ForecastResponse)
async def create_forecast(request: ForecastRequest):
    """Создание прогноза потребления."""
    # TODO: Implement forecasting
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Forecasting not implemented yet"
    )


@router.get("/{mcd_id}")
async def get_forecast(mcd_id: str, horizon_hours: int = 24):
    """Получение существующего прогноза."""
    # TODO: Implement forecast retrieval
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Forecast retrieval not implemented yet"
    )
