from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class RiskTrajectoryPoint(BaseModel):
    transaction_id: str
    timestamp: str
    amount: float
    currency: str = "INR"
    city: str
    risk_score: float
    risk_level: str
    action_taken: str
    signals: List[str]
    device_id: str
    is_new_device: bool = False

class RiskEvolutionTrajectory(BaseModel):
    account_id: str
    trajectory_levels: List[str] = Field(description="e.g. ['LOW', 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL']")
    score_history: List[float]
    is_escalating: bool
    risk_growth_rate: float = Field(description="Escalation acceleration per step in points/tx")
    accumulated_signals: List[str] = Field(description="Cumulative set of unique anomaly codes")
    escalation_points_count: int
    avg_interval_seconds: Optional[float] = None
    timeline_points: List[RiskTrajectoryPoint]

class SignalConfluence(BaseModel):
    has_confluence: bool
    confluence_name: str
    compounding_multiplier: float
    combined_risk_boost: float
    contributing_signals: List[str]
    confidence_score: float
    description: str

class ChangePointAnalysis(BaseModel):
    regime_shift_detected: bool
    change_point_timestamp: Optional[str] = None
    change_point_tx_id: Optional[str] = None
    historical_avg_amount: float
    historical_typical_city: str
    recent_avg_amount: float
    deviation_magnitude: float
    affected_dimensions: List[str]
    narrative: str

class NetworkLink(BaseModel):
    connected_account_id: str
    relationship_type: str = Field(description="e.g. Shared Hardware Fingerprint, Beneficiary, Rapid Fund Transfer")
    shared_entity: str
    link_grade: str = Field(description="NORMAL, SUSPICIOUS_CONNECTION, HIGH_RISK_CLUSTER, POTENTIAL_COORDINATED_ACTIVITY")
    explanation: str

class CrossAccountPropagation(BaseModel):
    account_id: str
    network_exposure_score: float
    cluster_classification: str = Field(description="NORMAL, SUSPICIOUS_CONNECTION, HIGH_RISK_CLUSTER, POTENTIAL_COORDINATED_ACTIVITY")
    correlated_accounts_count: int
    shared_devices: List[str]
    network_links: List[NetworkLink]

class FraudPatternHypothesis(BaseModel):
    pattern_id: str
    pattern_name: str
    pattern_type: str
    confidence_score: float
    primary_evidence: List[str]
    investigative_hypothesis: str

class ExplainableFraudStory(BaseModel):
    timeline: str
    behaviour_change: str
    signal_confluence: str
    network_relationship: str
    risk_escalation: str
    current_assessment: str
    recommended_action: str
    full_narrative: str

class InvestigationSummary(BaseModel):
    account_id: str
    holder_name: str
    primary_bank: str
    current_risk_score: float
    current_risk_level: str
    investigation_priority: str = Field(description="NORMAL, WATCH, INVESTIGATE, URGENT")
    priority_score: float
    detected_pattern: str
    is_escalating: bool
    last_active: str
    total_transactions_analyzed: int

class InvestigationDossier(BaseModel):
    summary: InvestigationSummary
    evolution: RiskEvolutionTrajectory
    confluence: SignalConfluence
    change_point: ChangePointAnalysis
    network_propagation: CrossAccountPropagation
    patterns: List[FraudPatternHypothesis]
    fraud_story: ExplainableFraudStory
