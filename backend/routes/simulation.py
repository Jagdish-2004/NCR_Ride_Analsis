from fastapi import APIRouter
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from backend.simulation.engine import generate_and_insert_ride

router = APIRouter()
scheduler = AsyncIOScheduler()

# Add the job in a paused state or start when requested
scheduler.add_job(generate_and_insert_ride, 'interval', seconds=5, id='ride_simulation')

@router.post("/start-simulation")
async def start_simulation():
    if not scheduler.running:
        scheduler.start()
        return {"message": "Simulation started."}
    else:
        scheduler.resume()
        return {"message": "Simulation resumed."}

@router.post("/stop-simulation")
async def stop_simulation():
    if scheduler.running:
        scheduler.pause()
        return {"message": "Simulation stopped."}
    return {"message": "Simulation is not running."}
