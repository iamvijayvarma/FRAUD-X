from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List, Dict, Any

from app.database import get_db
from app.models.account import Account
from app.models.device import AccountDevice, Device
from app.models.transaction import Transaction

router = APIRouter(prefix="/accounts", tags=["Accounts"])

@router.get("")
async def list_accounts(
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
) -> List[Dict[str, Any]]:
    """Lists accounts with their behavioral spending baselines and status."""
    stmt = select(Account).limit(limit)
    accounts = (await db.execute(stmt)).scalars().all()
    
    return [
        {
            "id": acc.id,
            "holder_name": acc.holder_name,
            "email": acc.email,
            "avg_amount": acc.avg_amount,
            "std_amount": acc.std_amount,
            "typical_city": acc.typical_city,
            "typical_country": acc.typical_country,
            "status": acc.status,
            "risk_rating": acc.risk_rating
        }
        for acc in accounts
    ]

@router.get("/{account_id}")
async def get_account_profile(account_id: str, db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    """Fetches detailed profile, known devices, and recent transactions for an account."""
    stmt = select(Account).where(Account.id == account_id)
    acc = (await db.execute(stmt)).scalar_one_or_none()
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")

    # Devices
    dev_stmt = select(Device).join(AccountDevice).where(AccountDevice.account_id == account_id)
    devices = (await db.execute(dev_stmt)).scalars().all()

    # Recent transactions
    tx_stmt = select(Transaction).where(Transaction.account_id == account_id).order_by(desc(Transaction.timestamp)).limit(10)
    txs = (await db.execute(tx_stmt)).scalars().all()

    return {
        "account": {
            "id": acc.id,
            "holder_name": acc.holder_name,
            "email": acc.email,
            "avg_amount": acc.avg_amount,
            "std_amount": acc.std_amount,
            "typical_city": acc.typical_city,
            "typical_country": acc.typical_country,
            "typical_location_lat": acc.typical_location_lat,
            "typical_location_lon": acc.typical_location_lon,
            "status": acc.status,
            "risk_rating": acc.risk_rating
        },
        "devices": [
            {
                "id": d.id,
                "browser_os": d.browser_os,
                "first_seen": d.first_seen.isoformat() if d.first_seen else None,
                "is_proxy": d.is_known_proxy
            }
            for d in devices
        ],
        "recent_transactions": [
            {
                "id": t.id,
                "timestamp": t.timestamp.isoformat(),
                "amount": t.amount,
                "merchant": t.merchant_name,
                "risk_score": t.risk_score,
                "risk_level": t.risk_level,
                "action": t.action_taken
            }
            for t in txs
        ]
    }
