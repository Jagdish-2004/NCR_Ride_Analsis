from fastapi import APIRouter, Depends, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List, Optional
from datetime import datetime
from backend.database import get_db
from backend.models.ride import RideModel

router = APIRouter()

@router.post("/", response_model=RideModel)
async def create_ride(ride: RideModel, db: AsyncIOMotorDatabase = Depends(get_db)):
    ride_dict = ride.model_dump()
    await db.rides.insert_one(ride_dict)
    return ride

@router.get("/", response_model=List[RideModel])
async def get_rides(
    skip: int = 0, 
    limit: int = 100,
    status: Optional[str] = None,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    query = {}
    if status:
        query["booking_status"] = status
    
    cursor = db.rides.find(query).skip(skip).limit(limit).sort("pickup_time", -1)
    rides = await cursor.to_list(length=limit)
    return rides

@router.get("/{ride_id}", response_model=RideModel)
async def get_ride(ride_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    ride = await db.rides.find_one({"ride_id": ride_id})
    if ride:
        return ride
    raise HTTPException(status_code=404, detail="Ride not found")

@router.put("/{ride_id}", response_model=RideModel)
async def update_ride(ride_id: str, ride_update: dict, db: AsyncIOMotorDatabase = Depends(get_db)):
    result = await db.rides.update_one({"ride_id": ride_id}, {"$set": ride_update})
    if result.modified_count:
        updated_ride = await db.rides.find_one({"ride_id": ride_id})
        return updated_ride
    raise HTTPException(status_code=404, detail="Ride not found or no changes made")

@router.delete("/{ride_id}")
async def delete_ride(ride_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    result = await db.rides.delete_one({"ride_id": ride_id})
    if result.deleted_count:
        return {"message": "Ride deleted successfully"}
    raise HTTPException(status_code=404, detail="Ride not found")
