from motor.motor_asyncio import AsyncIOMotorDatabase

async def get_peak_hours(db: AsyncIOMotorDatabase):
    pipeline = [
        {"$group": {"_id": "$pickup_hour", "total_rides": {"$sum": 1}}},
        {"$sort": {"total_rides": -1}}
    ]
    cursor = db.rides.aggregate(pipeline)
    return await cursor.to_list(length=24)

async def get_demand_by_day(db: AsyncIOMotorDatabase):
    pipeline = [
        {"$group": {"_id": "$pickup_day_of_week", "total_rides": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]
    cursor = db.rides.aggregate(pipeline)
    return await cursor.to_list(length=7)

async def get_fare_analysis(db: AsyncIOMotorDatabase):
    pipeline = [
        {
            "$bucket": {
                "groupBy": "$trip_distance",
                "boundaries": [0, 5, 10, 15, 20, 50, 100],
                "default": "100+",
                "output": {
                    "avg_fare": {"$avg": "$fare_amount"},
                    "count": {"$sum": 1}
                }
            }
        }
    ]
    cursor = db.rides.aggregate(pipeline)
    return await cursor.to_list(length=10)

async def get_cancellation_rate(db: AsyncIOMotorDatabase):
    pipeline = [
        {"$group": {"_id": "$booking_status", "count": {"$sum": 1}}}
    ]
    cursor = db.rides.aggregate(pipeline)
    return await cursor.to_list(length=10)
