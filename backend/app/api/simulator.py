from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import Dict, Any

from app.database import get_db, init_db
from app.schemas.simulator import ScenarioTriggerRequest, SimulatorControlRequest, SimulatorStatusResponse
from app.services.simulator import simulator_service
from app.utils.seed_data import seed_database
from app.websocket.connection_manager import manager

router = APIRouter(prefix="/simulator", tags=["Attack Simulator"])

@router.get("/status", response_model=SimulatorStatusResponse)
async def get_simulator_status():
    """Returns current status of the attack simulator."""
    status = simulator_service.get_status()
    return SimulatorStatusResponse(**status)

@router.post("/scenario")
async def trigger_scenario(req: ScenarioTriggerRequest):
    """Triggers an instantaneous attack scenario sequence."""
    try:
        results = await simulator_service.trigger_scenario(
            scenario_name=req.scenario.upper(),
            target_account_id=req.target_account_id
        )
        # Notify WebSocket
        await manager.broadcast("SIMULATOR_STATE", simulator_service.get_status())
        return {
            "success": True,
            "scenario": req.scenario.upper(),
            "injected_count": len(results),
            "transactions": results
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/control")
async def control_simulator(req: SimulatorControlRequest):
    """Starts, stops, or configures the continuous simulator background stream."""
    action = req.action.upper()
    if action == "START":
        await simulator_service.start_stream(tps=req.tps or 1.0)
    elif action == "STOP":
        await simulator_service.stop_stream()
    else:
        raise HTTPException(status_code=400, detail="Invalid action. Use START or STOP.")

    status = simulator_service.get_status()
    await manager.broadcast("SIMULATOR_STATE", status)
    return status

@router.post("/reset")
async def reset_simulation_state(db: AsyncSession = Depends(get_db)):
    """Stops simulator, clears alerts and test transactions, and re-seeds baseline."""
    await simulator_service.stop_stream()
    simulator_service.total_injected = 0

    # Delete non-historical transactions and alerts
    await db.execute(text("DELETE FROM alerts;"))
    await db.execute(text("DELETE FROM transactions WHERE id NOT LIKE 'TX-HIST-%';"))
    await db.commit()

    # Re-seed baseline if needed
    await seed_database(db)

    status = simulator_service.get_status()
    await manager.broadcast("SIMULATOR_STATE", status)
    return {"success": True, "message": "Simulation environment reset to baseline."}
