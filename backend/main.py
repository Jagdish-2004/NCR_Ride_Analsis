from fastapi import FastAPI
from backend.routes import rides, analytics, simulation
from backend.database import db

app = FastAPI(title="Ride Demand Analyzer API")

app.include_router(rides.router, prefix="/ride", tags=["Rides"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
app.include_router(simulation.router, tags=["Simulation"])

@app.on_event("startup")
async def startup_db_client():
    # Create indexes on startup
    await db.rides.create_index("pickup_time")
    await db.rides.create_index("booking_status")
    await db.rides.create_index("pickup_location")

@app.get("/")
async def root():
    return {"message": "Welcome to Ride Demand Analyzer API"}
