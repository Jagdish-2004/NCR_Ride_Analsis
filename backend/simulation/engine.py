import random
import uuid
import logging
from datetime import datetime
from backend.database import db
from backend.models.ride import RideModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

LOCATIONS = [
    "Connaught Place", "Cyber City", "Indirapuram", "Noida Sector 18", 
    "Vasant Kunj", "Saket", "Dwarka", "Gurgaon Sector 29", "Aerocity"
]

VEHICLES = ["Auto", "Go Mini", "Go Sedan", "Bike", "Premier Sedan", "eBike", "Uber XL"]
PAYMENTS = ["UPI", "Cash", "Uber Wallet", "Credit Card", "Debit Card"]
CANCEL_REASONS = ["Change of plans", "Driver asked to cancel", "Wrong Address", "Driver is not moving towards pickup location", "AC is not working"]
STATUSES = ["Completed", "Cancelled by Driver", "Cancelled by Customer", "No Driver Found", "Incomplete"]

async def generate_and_insert_ride():
    try:
        pickup_loc = random.choice(LOCATIONS)
        drop_loc = random.choice([loc for loc in LOCATIONS if loc != pickup_loc])
        distance = round(random.uniform(2.0, 35.0), 2)
        fare = round(distance * random.uniform(12.0, 20.0), 2) # 12 to 20 Rs per km
        status = random.choices(STATUSES, weights=[0.62, 0.18, 0.07, 0.07, 0.06])[0]
        vehicle = random.choices(VEHICLES, weights=[0.25, 0.20, 0.18, 0.15, 0.12, 0.07, 0.03])[0]
        payment = random.choices(PAYMENTS, weights=[0.45, 0.25, 0.12, 0.10, 0.08])[0]
        
        cancel_reason = None
        if status in ["Cancelled by Customer", "Cancelled by Driver"]:
            cancel_reason = random.choice(CANCEL_REASONS)

        now = datetime.utcnow()
        ride = RideModel(
            ride_id=str(uuid.uuid4()),
            pickup_date=now.strftime("%m/%d/%Y"),
            pickup_time=now.strftime("%H:%M:%S"),
            pickup_hour=now.hour,
            pickup_day_of_week=now.weekday(),
            pickup_location=pickup_loc,
            drop_location=drop_loc,
            trip_distance=distance,
            fare_amount=fare,
            booking_status=status,
            vehicle_type=vehicle,
            payment_method=payment,
            cancellation_reason=cancel_reason,
            driver_rating=round(random.uniform(3.5, 5.0), 1) if status == "Completed" else None,
            customer_rating=round(random.uniform(3.5, 5.0), 1) if status == "Completed" else None
        )
        
        await db.rides.insert_one(ride.model_dump())
        logger.info(f"Simulated ride inserted: {ride.ride_id}")
        
    except Exception as e:
        logger.error(f"Error in simulation: {e}")
