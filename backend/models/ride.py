from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class RideModel(BaseModel):
    ride_id: str
    pickup_date: str
    pickup_time: str
    pickup_hour: int
    pickup_day_of_week: int
    drop_time: Optional[datetime] = None
    pickup_location: str
    drop_location: str
    trip_distance: float
    fare_amount: float
    booking_status: str
    vehicle_type: str
    payment_method: Optional[str] = None
    cancellation_reason: Optional[str] = None
    driver_rating: Optional[float] = None
    customer_rating: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
