from pydantic import BaseModel, Field
from typing import Optional, List

class ScenarioTriggerRequest(BaseModel):
    scenario: str # ATO, IMPOSSIBLE_TRAVEL, CARD_TESTING, WHALE_OUTLIER, MULE_RING, NORMAL_FLOW
    target_account_id: Optional[str] = None
    burst_count: Optional[int] = 5

class SimulatorControlRequest(BaseModel):
    action: str # START, STOP, RESET
    tps: Optional[float] = Field(1.0, ge=0.2, le=20.0)

class SimulatorStatusResponse(BaseModel):
    is_running: bool
    current_tps: float
    total_injected: int
    active_scenario: Optional[str] = None
    status_message: str
