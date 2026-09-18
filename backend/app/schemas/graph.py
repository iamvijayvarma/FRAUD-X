from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class GraphNode(BaseModel):
    id: str
    label: str
    type: str # ACCOUNT, DEVICE, MERCHANT, IP
    risk_level: str # LOW, MEDIUM, HIGH, CRITICAL
    degree: int = 1
    properties: Dict[str, Any] = {}

class GraphEdge(BaseModel):
    source: str
    target: str
    type: str # TRANSFERRED_TO, USED_DEVICE, TRANSACTED_AT
    amount: Optional[float] = None
    timestamp: Optional[str] = None
    is_circular: bool = False

class GraphNetworkResponse(BaseModel):
    nodes: List[GraphNode]
    edges: List[GraphEdge]
    cycles_detected: List[List[str]] = []
    suspicious_clusters_count: int = 0
