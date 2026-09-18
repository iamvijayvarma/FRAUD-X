from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class SignalEvidence(BaseModel):
    code: str
    name: str
    category: str # BEHAVIORAL, DEVICE, LOCATION, VELOCITY, GRAPH, ML
    points: float
    observed_value: str
    baseline_value: str
    severity: str # INFO, WARNING, CRITICAL
    description: str

class RiskAssessment(BaseModel):
    transaction_id: str
    risk_score: float = Field(..., ge=0.0, le=100.0)
    risk_level: str # LOW, MEDIUM, HIGH, CRITICAL
    action_taken: str # ALLOW, MONITOR, CHALLENGE, HOLD, BLOCK
    primary_reasons: List[str]
    signals: List[SignalEvidence]
    ml_score: float = 0.0
    velocity_count_1m: int = 0
    velocity_count_5m: int = 0
    speed_kmh: Optional[float] = None
    distance_km: Optional[float] = None
    device_account_count: int = 1
    is_circular_loop: bool = False

class AINarrativeReport(BaseModel):
    transaction_id: str
    executive_summary: str
    forensic_narrative: str
    correlation_analysis: str
    recommended_action: str
    confidence_score: float
    action_justification: str
    immediate_mitigations: List[str]
    timestamp: str
