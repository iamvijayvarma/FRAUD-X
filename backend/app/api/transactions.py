from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func
from typing import Optional, List
import json

from app.database import get_db
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionResponse, TransactionListResponse
from app.schemas.risk import RiskAssessment
from app.services.context_engine import context_engine
from app.websocket.connection_manager import manager

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("/ingest", response_model=TransactionResponse)
async def ingest_transaction(
    tx_in: TransactionCreate,
    db: AsyncSession = Depends(get_db)
):
    """Processes a live transaction through the entire multi-engine intelligence pipeline."""
    tx_obj, assessment, ai_report = await context_engine.process_transaction(db, tx_in)
    
    # Broadcast to WebSocket
    await manager.broadcast("TX_PROCESSED", {
        "id": tx_obj.id,
        "timestamp": tx_obj.timestamp.isoformat(),
        "account_id": tx_obj.account_id,
        "target_account_id": tx_obj.target_account_id,
        "amount": tx_obj.amount,
        "currency": tx_obj.currency,
        "merchant_name": tx_obj.merchant_name,
        "merchant_category": tx_obj.merchant_category,
        "device_id": tx_obj.device_id,
        "location_city": tx_obj.location_city,
        "location_country": tx_obj.location_country,
        "location_lat": tx_obj.location_lat,
        "location_lon": tx_obj.location_lon,
        "risk_score": assessment.risk_score,
        "risk_level": assessment.risk_level,
        "action_taken": assessment.action_taken,
        "assessment": assessment.model_dump(),
        "ai_narrative": ai_report.model_dump()
    })

    resp = TransactionResponse.model_validate(tx_obj)
    resp.assessment = assessment
    return resp

@router.get("", response_model=TransactionListResponse)
async def list_transactions(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    min_risk: Optional[float] = Query(None, ge=0.0, le=100.0),
    risk_level: Optional[str] = None,
    account_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Lists transactions with filtering by risk level, minimum score, and account."""
    query = select(Transaction)
    count_query = select(func.count(Transaction.id))

    if min_risk is not None:
        query = query.where(Transaction.risk_score >= min_risk)
        count_query = count_query.where(Transaction.risk_score >= min_risk)
    if risk_level:
        query = query.where(Transaction.risk_level == risk_level.upper())
        count_query = count_query.where(Transaction.risk_level == risk_level.upper())
    if account_id:
        query = query.where(Transaction.account_id == account_id)
        count_query = count_query.where(Transaction.account_id == account_id)

    total = (await db.execute(count_query)).scalar() or 0
    query = query.order_by(desc(Transaction.timestamp)).offset(offset).limit(limit)
    
    rows = (await db.execute(query)).scalars().all()
    
    results = []
    for r in rows:
        item = TransactionResponse.model_validate(r)
        if r.evidence_json:
            try:
                item.assessment = RiskAssessment.model_validate_json(r.evidence_json)
            except Exception:
                pass
        results.append(item)

    return TransactionListResponse(total=total, transactions=results)

@router.get("/{tx_id}", response_model=TransactionResponse)
async def get_transaction(tx_id: str, db: AsyncSession = Depends(get_db)):
    """Fetches detailed forensic dossier for a specific transaction."""
    stmt = select(Transaction).where(Transaction.id == tx_id)
    tx = (await db.execute(stmt)).scalar_one_or_none()
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    item = TransactionResponse.model_validate(tx)
    if tx.evidence_json:
        try:
            item.assessment = RiskAssessment.model_validate_json(tx.evidence_json)
        except Exception:
            pass
    return item
