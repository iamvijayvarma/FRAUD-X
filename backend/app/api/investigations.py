from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.schemas.investigation import (
    InvestigationSummary,
    InvestigationDossier,
    RiskEvolutionTrajectory,
    FraudPatternHypothesis,
    RiskTrajectoryPoint
)
from app.services.contextual_fusion import contextual_fraud_evolution

router = APIRouter(prefix="/investigations", tags=["Investigations"])

@router.get("", response_model=List[InvestigationSummary])
async def list_investigations(
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """List all accounts ranked by Adaptive Investigation Priority (URGENT -> INVESTIGATE -> WATCH -> NORMAL)."""
    return await contextual_fraud_evolution.list_active_investigations(db, limit=limit)

@router.get("/{account_id}", response_model=InvestigationDossier)
async def get_investigation_dossier(
    account_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Fetch complete Contextual Fraud Evolution Dossier for an account."""
    dossier = await contextual_fraud_evolution.analyze_account(account_id, db)
    if not dossier:
        raise HTTPException(status_code=404, detail=f"Account {account_id} not found")
    return dossier

@router.get("/{account_id}/evolution", response_model=RiskEvolutionTrajectory)
async def get_account_evolution(
    account_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Fetch temporal risk evolution trajectory for an account."""
    dossier = await contextual_fraud_evolution.analyze_account(account_id, db)
    if not dossier:
        raise HTTPException(status_code=404, detail=f"Account {account_id} not found")
    return dossier.evolution

@router.get("/{account_id}/timeline", response_model=List[RiskTrajectoryPoint])
async def get_account_timeline(
    account_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Fetch chronological risk points timeline for an account."""
    dossier = await contextual_fraud_evolution.analyze_account(account_id, db)
    if not dossier:
        raise HTTPException(status_code=404, detail=f"Account {account_id} not found")
    return dossier.evolution.timeline_points

@router.get("/{account_id}/patterns", response_model=List[FraudPatternHypothesis])
async def get_account_patterns(
    account_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Fetch synthesized fraud pattern hypotheses for an account."""
    dossier = await contextual_fraud_evolution.analyze_account(account_id, db)
    if not dossier:
        raise HTTPException(status_code=404, detail=f"Account {account_id} not found")
    return dossier.patterns

@router.post("/judge-demo", response_model=InvestigationDossier)
async def trigger_judge_demo_scenario(
    db: AsyncSession = Depends(get_db)
):
    """
    Triggers the Judge Demonstration Scenario on ACC-IN-1043:
    T1: ₹2,500 (Coimbatore, Known device) -> LOW
    T2: ₹35,000 (Coimbatore, New device) -> MEDIUM
    T3: ₹85,000 (Mumbai, Impossible travel) -> HIGH
    T4: ₹1,20,000 (New Delhi, Rapid velocity) -> CRITICAL
    Cross-account device linkage to ACC-IN-1002.
    Returns complete Investigation Dossier ready for immediate visualization.
    """
    return await contextual_fraud_evolution.run_judge_demo(db)

@router.post("/judge-demo/reset", response_model=InvestigationDossier)
async def reset_judge_demo_scenario(
    db: AsyncSession = Depends(get_db)
):
    """
    Resets the Judge Demonstration Scenario on ACC-IN-1043 back to initial clean baseline.
    Removes attack transactions, clears syndicate device links, and restores 1 clean baseline transaction.
    """
    return await contextual_fraud_evolution.reset_judge_demo(db)

