from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from backend.database import get_db
from backend.services import analytics_service

router = APIRouter()

@router.get("/peak-hours")
async def peak_hours(db: AsyncIOMotorDatabase = Depends(get_db)):
    return await analytics_service.get_peak_hours(db)

@router.get("/demand-by-day")
async def demand_by_day(db: AsyncIOMotorDatabase = Depends(get_db)):
    return await analytics_service.get_demand_by_day(db)

@router.get("/fare-analysis")
async def fare_analysis(db: AsyncIOMotorDatabase = Depends(get_db)):
    return await analytics_service.get_fare_analysis(db)

@router.get("/cancellation-rate")
async def cancellation_rate(db: AsyncIOMotorDatabase = Depends(get_db)):
    return await analytics_service.get_cancellation_rate(db)
