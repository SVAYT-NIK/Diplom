"""
Ingest endpoints for receiving metering and weather data.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter()


class MeteringDataPoint(BaseModel):
    device_id: str
    timestamp: datetime
    value: float
    unit: str = "kWh"
    quality: Optional[str] = "good"


class WeatherDataPoint(BaseModel):
    location_id: str
    timestamp: datetime
    temperature: float
    humidity: Optional[float] = None
    pressure: Optional[float] = None


@router.post("/metering", response_model=dict)
async def ingest_metering(data: List[MeteringDataPoint]):
    """Приём данных с приборов учёта."""
    # TODO: Implement data ingestion
    return {"status": "accepted", "count": len(data)}


@router.post("/weather", response_model=dict)
async def ingest_weather(data: List[WeatherDataPoint]):
    """Приём погодных данных."""
    # TODO: Implement weather data ingestion
    return {"status": "accepted", "count": len(data)}


@router.get("/status/{device_id}")
async def get_device_status(device_id: str):
    """Получение статуса устройства."""
    # TODO: Implement status retrieval
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Device status not implemented yet"
    )
