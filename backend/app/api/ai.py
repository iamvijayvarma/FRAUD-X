from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.transaction import Transaction
from app.models.account import Account
from app.schemas.risk import RiskAssessment, AINarrativeReport
from app.services.ai_analyst import ai_analyst

router = APIRouter(prefix="/ai", tags=["AI Fraud Analyst"])

@router.post("/investigate/{tx_id}", response_model=AINarrativeReport)
async def investigate_transaction(tx_id: str, db: AsyncSession = Depends(get_db)):
    """Runs on-demand AI forensic analysis on a specific transaction."""
    stmt = select(Transaction).where(Transaction.id == tx_id)
    tx = (await db.execute(stmt)).scalar_one_or_none()
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")

    acc_stmt = select(Account).where(Account.id == tx.account_id)
    account = (await db.execute(acc_stmt)).scalar_one_or_none()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    if not tx.evidence_json:
        raise HTTPException(status_code=400, detail="Transaction has no evidence payload")

    assessment = RiskAssessment.model_validate_json(tx.evidence_json)
    report = await ai_analyst.investigate(tx, account, assessment)
    
    # Cache to database
    tx.ai_narrative = report.model_dump_json()
    await db.commit()

    return report
