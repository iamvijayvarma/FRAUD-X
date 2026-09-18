from fastapi import APIRouter, Query
from typing import Optional
from app.schemas.graph import GraphNetworkResponse
from app.services.graph_service import graph_service

router = APIRouter(prefix="/graph", tags=["Graph Network"])

@router.get("/network", response_model=GraphNetworkResponse)
async def get_network_graph(
    center_id: Optional[str] = Query(None, description="Center node for ego network focus"),
    max_nodes: int = Query(45, ge=10, le=100)
):
    """Exports active network topology (accounts, shared devices, merchants, and cycles)."""
    return graph_service.export_subgraph(center_id=center_id, max_nodes=max_nodes)
