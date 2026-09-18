from datetime import datetime
from typing import Tuple, List, Set, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
import json
import logging

from app.models.account import Account
from app.models.device import Device, AccountDevice
from app.models.transaction import Transaction
from app.models.alert import Alert
from app.schemas.transaction import TransactionCreate
from app.schemas.risk import RiskAssessment, SignalEvidence, AINarrativeReport

from app.services.behavioral import behavioral_engine
from app.services.device_intelligence import device_intelligence
from app.services.location import location_engine
from app.services.velocity import velocity_engine
from app.services.graph_service import graph_service
from app.services.ml_anomaly import ml_engine
from app.services.risk_fusion import risk_fusion
from app.services.ai_analyst import ai_analyst

logger = logging.getLogger("fraud_x.context_engine")

class ContextIntelligenceEngine:
    """
    Master context orchestration engine.
    Fetches multi-dimensional account context and coordinates intelligence engines.
    """

    async def process_transaction(
        self,
        db: AsyncSession,
        tx_in: TransactionCreate
    ) -> Tuple[Transaction, RiskAssessment, AINarrativeReport]:
        now = tx_in.timestamp or datetime.utcnow()

        # 1. Fetch or create Account
        stmt = select(Account).where(Account.id == tx_in.account_id)
        res = await db.execute(stmt)
        account = res.scalar_one_or_none()
        if not account:
            account = Account(
                id=tx_in.account_id,
                holder_name=f"User {tx_in.account_id}",
                email=f"{tx_in.account_id.lower()}@example.com",
                avg_amount=tx_in.amount,
                std_amount=tx_in.amount * 0.25,
                typical_city=tx_in.location_city,
                typical_country=tx_in.location_country,
                typical_location_lat=tx_in.location_lat,
                typical_location_lon=tx_in.location_lon
            )
            db.add(account)
            await db.flush()

        # 2. Fetch or create Device record
        dev_stmt = select(Device).where(Device.id == tx_in.device_id)
        dev_res = await db.execute(dev_stmt)
        device = dev_res.scalar_one_or_none()
        if not device:
            device = Device(
                id=tx_in.device_id,
                first_seen=now,
                last_seen=now,
                browser_os="Client Web/Mobile Agent"
            )
            db.add(device)
            await db.flush()
        else:
            device.last_seen = now

        # 3. Fetch known devices for this account
        acc_devs_stmt = select(AccountDevice.device_id).where(AccountDevice.account_id == account.id)
        acc_devs_res = await db.execute(acc_devs_stmt)
        known_devices: Set[str] = set(acc_devs_res.scalars().all())

        # 4. Count distinct accounts associated with this device
        share_stmt = select(func.count(func.distinct(AccountDevice.account_id))).where(AccountDevice.device_id == tx_in.device_id)
        share_res = await db.execute(share_stmt)
        dev_account_count = max(1, share_res.scalar() or 1)

        # 5. Fetch recent transactions for this account (last 50)
        recent_tx_stmt = select(Transaction).where(
            Transaction.account_id == account.id
        ).order_by(desc(Transaction.timestamp)).limit(50)
        recent_res = await db.execute(recent_tx_stmt)
        recent_transactions = list(recent_res.scalars().all())
        last_tx = recent_transactions[0] if recent_transactions else None
        recent_categories = [t.merchant_category for t in recent_transactions if t.merchant_category]

        # 6. Execute Modular Intelligence Engines
        all_signals: List[SignalEvidence] = []

        # A. Behavioral
        beh_signals = behavioral_engine.evaluate(
            account=account,
            amount=tx_in.amount,
            merchant_category=tx_in.merchant_category,
            timestamp=now,
            recent_categories=recent_categories
        )
        all_signals.extend(beh_signals)

        # B. Device Intelligence
        dev_signals = device_intelligence.evaluate(
            device_id=tx_in.device_id,
            known_account_device_ids=known_devices,
            total_accounts_linked_to_device=dev_account_count,
            device_record=device
        )
        all_signals.extend(dev_signals)

        # C. Location Intelligence
        loc_signals, speed_kmh, dist_km = location_engine.evaluate(
            account=account,
            current_lat=tx_in.location_lat,
            current_lon=tx_in.location_lon,
            current_city=tx_in.location_city,
            current_time=now,
            last_transaction=last_tx
        )
        all_signals.extend(loc_signals)

        # D. Velocity Analysis
        vel_signals, count_1m, count_5m = velocity_engine.evaluate(
            current_time=now,
            current_amount=tx_in.amount,
            recent_transactions=recent_transactions
        )
        all_signals.extend(vel_signals)

        # E. Graph Intelligence
        graph_signals, is_circular, graph_share_count = graph_service.evaluate(
            account_id=account.id,
            target_account_id=tx_in.target_account_id,
            device_id=tx_in.device_id
        )
        all_signals.extend(graph_signals)
        effective_share_count = max(dev_account_count, graph_share_count)

        # F. ML Isolation Forest Anomaly
        z_score = (tx_in.amount - account.avg_amount) / max(account.std_amount, 5.0)
        ml_score, ml_signals = ml_engine.score_transaction(
            amount=tx_in.amount,
            z_score=z_score,
            vel_1m=count_1m,
            vel_5m=count_5m,
            speed_kmh=speed_kmh or 0.0,
            dev_share_count=effective_share_count,
            hour=now.hour
        )
        all_signals.extend(ml_signals)

        # 7. Risk Fusion & Decisioning
        assessment = risk_fusion.fuse(
            transaction_id="", # Assigned below
            signals=all_signals,
            ml_score=ml_score,
            speed_kmh=speed_kmh,
            dist_km=dist_km,
            count_1m=count_1m,
            count_5m=count_5m,
            share_count=effective_share_count,
            is_circular=is_circular
        )

        # 8. Persist Transaction
        tx_obj = Transaction(
            timestamp=now,
            account_id=account.id,
            target_account_id=tx_in.target_account_id,
            amount=tx_in.amount,
            currency=tx_in.currency,
            merchant_name=tx_in.merchant_name,
            merchant_category=tx_in.merchant_category,
            transaction_type=tx_in.transaction_type,
            device_id=tx_in.device_id,
            ip_address=tx_in.ip_address,
            location_city=tx_in.location_city,
            location_country=tx_in.location_country,
            location_lat=tx_in.location_lat,
            location_lon=tx_in.location_lon,
            risk_score=assessment.risk_score,
            risk_level=assessment.risk_level,
            action_taken=assessment.action_taken,
            evidence_json=assessment.model_dump_json(),
            is_synthetic=True
        )
        db.add(tx_obj)
        await db.flush() # Generates tx_obj.id

        # Update assessment with generated transaction_id
        assessment.transaction_id = tx_obj.id

        # 9. Link AccountDevice if new
        if tx_in.device_id not in known_devices:
            link = AccountDevice(
                account_id=account.id,
                device_id=tx_in.device_id,
                first_used_at=now,
                last_used_at=now,
                usage_count=1
            )
            db.add(link)

        # 10. Update Graph Service
        graph_service.record_transaction(
            account_id=account.id,
            target_account_id=tx_in.target_account_id,
            merchant_name=tx_in.merchant_name,
            amount=tx_in.amount,
            timestamp=now.isoformat(),
            device_id=tx_in.device_id,
            risk_level=assessment.risk_level
        )

        # 11. Generate AI Analyst Narrative
        ai_report = await ai_analyst.investigate(tx_obj, account, assessment)
        tx_obj.ai_narrative = ai_report.model_dump_json()

        # 12. Create Alert if HIGH or CRITICAL
        if assessment.risk_level in ["HIGH", "CRITICAL"]:
            alert = Alert(
                transaction_id=tx_obj.id,
                account_id=account.id,
                created_at=now,
                risk_score=assessment.risk_score,
                risk_level=assessment.risk_level,
                status="OPEN",
                summary=assessment.primary_reasons[0] if assessment.primary_reasons else "High risk detected",
                ai_summary=ai_report.executive_summary
            )
            db.add(alert)

        await db.commit()
        await db.refresh(tx_obj)

        return tx_obj, assessment, ai_report

context_engine = ContextIntelligenceEngine()
