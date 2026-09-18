from typing import List, Optional
from datetime import datetime, timedelta
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.models.account import Account
from app.models.device import Device, AccountDevice
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate
from app.services.context_engine import context_engine

from app.schemas.investigation import (
    InvestigationDossier,
    InvestigationSummary,
    RiskEvolutionTrajectory,
    SignalConfluence,
    ChangePointAnalysis,
    CrossAccountPropagation,
    FraudPatternHypothesis,
    ExplainableFraudStory
)
from app.services.risk_evolution import risk_evolution_engine
from app.services.signal_confluence import signal_confluence_engine
from app.services.change_point import change_point_engine
from app.services.cross_account_propagation import cross_account_propagation_engine
from app.services.pattern_engine import pattern_engine
from app.services.fraud_story import fraud_story_engine
from app.services.investigation_priority import investigation_priority_engine

class ContextualFraudEvolutionService:
    """
    Core Innovation Orchestration Service:
    Synthesizes temporal risk evolution, signal confluence, change-point analysis,
    cross-account network propagation, pattern formation, and explainable fraud narratives.
    """

    @staticmethod
    async def analyze_account(account_id: str, db: AsyncSession) -> Optional[InvestigationDossier]:
        # 1. Fetch Account
        acc_stmt = select(Account).where(Account.id == account_id)
        res = await db.execute(acc_stmt)
        account = res.scalar_one_or_none()
        if not account:
            return None

        # 2. Fetch all chronological transactions
        tx_stmt = select(Transaction).where(
            Transaction.account_id == account_id
        ).order_by(Transaction.timestamp.asc())
        tx_res = await db.execute(tx_stmt)
        transactions = list(tx_res.scalars().all())

        latest_tx = transactions[-1] if transactions else None

        # 3. Innovation 1: Temporal Risk Evolution
        evolution = risk_evolution_engine.analyze_trajectory(account_id, transactions)

        # 4. Innovation 2: Signal Confluence
        confluence = signal_confluence_engine.evaluate(evolution.accumulated_signals)

        # 5. Innovation 4: Behavioural Change-Point Detection
        change_point = change_point_engine.detect_change_point(account, transactions)

        # 6. Innovation 3: Cross-Account Context Propagation
        network = await cross_account_propagation_engine.analyze(account_id, db)

        # 7. Innovation 5: Fraud Pattern Formation
        patterns = pattern_engine.synthesize_patterns(evolution, confluence, change_point, network)

        # 8. Innovation 6: Explainable Fraud Story
        fraud_story = fraud_story_engine.generate_story(
            account=account,
            evolution=evolution,
            confluence=confluence,
            change_point=change_point,
            network=network,
            patterns=patterns,
            latest_tx=latest_tx
        )

        # 9. Innovation 7: Adaptive Investigation Priority
        cur_score = evolution.score_history[-1] if evolution.score_history else 0.0
        priority_tier, priority_score = investigation_priority_engine.calculate_priority(
            current_risk_score=cur_score,
            is_escalating=evolution.is_escalating,
            risk_growth_rate=evolution.risk_growth_rate,
            confluence=confluence,
            change_point=change_point,
            network=network,
            signals_count=len(evolution.accumulated_signals)
        )

        # 10. Assemble Composite Dossier
        summary = InvestigationSummary(
            account_id=account.id,
            holder_name=account.holder_name,
            primary_bank=account.primary_bank or "HDFC Bank",
            current_risk_score=cur_score,
            current_risk_level=evolution.trajectory_levels[-1] if evolution.trajectory_levels else "LOW",
            investigation_priority=priority_tier,
            priority_score=priority_score,
            detected_pattern=patterns[0].pattern_name if patterns else "None",
            is_escalating=evolution.is_escalating,
            last_active=latest_tx.timestamp.isoformat() if latest_tx else datetime.utcnow().isoformat(),
            total_transactions_analyzed=len(transactions)
        )

        return InvestigationDossier(
            summary=summary,
            evolution=evolution,
            confluence=confluence,
            change_point=change_point,
            network_propagation=network,
            patterns=patterns,
            fraud_story=fraud_story
        )

    @staticmethod
    async def list_active_investigations(db: AsyncSession, limit: int = 50) -> List[InvestigationSummary]:
        acc_stmt = select(Account).limit(limit)
        acc_res = await db.execute(acc_stmt)
        accounts = list(acc_res.scalars().all())

        summaries: List[InvestigationSummary] = []
        for acc in accounts:
            dossier = await ContextualFraudEvolutionService.analyze_account(acc.id, db)
            if dossier:
                summaries.append(dossier.summary)

        # Rank order by priority_score descending (URGENT -> INVESTIGATE -> WATCH -> NORMAL)
        summaries.sort(key=lambda s: s.priority_score, reverse=True)
        return summaries

    @staticmethod
    async def run_judge_demo(db: AsyncSession) -> InvestigationDossier:
        """
        Executes the Judge Demonstration Scenario:
        Account: ACC-IN-1043
        T1: ₹2,500, Coimbatore, UPI, Known device -> LOW
        T2: ₹35,000, New device, Coimbatore -> MEDIUM
        T3: ₹85,000, Mumbai, New device -> HIGH
        T4: ₹1,20,000, Delhi, Rapid transaction -> CRITICAL
        Meanwhile another account (ACC-IN-1002) shares the suspicious device.
        """
        target_id = "ACC-IN-1043"

        # Ensure account ACC-IN-1043 exists
        acc_res = await db.execute(select(Account).where(Account.id == target_id))
        target_account = acc_res.scalar_one_or_none()
        if not target_account:
            target_account = Account(
                id=target_id,
                holder_name="Sanjay Menon",
                email="sanjay.menon.1043@upi.in",
                avg_amount=3500.0,
                std_amount=950.0,
                typical_city="Coimbatore",
                typical_country="India",
                typical_location_lat=11.0168,
                typical_location_lon=76.9558,
                primary_bank="HDFC Bank",
                status="ACTIVE",
                risk_rating="LOW"
            )
            db.add(target_account)
            await db.flush()

        base_time = datetime.utcnow() - timedelta(minutes=15)
        known_dev = "DEV-IN-1043-PRIM"
        attack_dev = f"DEV-IN-ATTACK-SYNDICATE-{uuid.uuid4().hex[:6].upper()}"

        # Clean prior transactions on target_id to give pristine demonstration trajectory
        from sqlalchemy import delete
        await db.execute(delete(Transaction).where(Transaction.account_id == target_id))
        await db.flush()

        # Step 1: Normal Transaction T1 (Coimbatore, ₹2,500, Known device) -> LOW
        t1_in = TransactionCreate(
            account_id=target_id,
            amount=2500.0,
            currency="INR",
            merchant_name="A2B Sweets Coimbatore",
            merchant_category="FOOD_DELIVERY",
            transaction_type="UPI",
            bank_name="HDFC Bank",
            device_id=known_dev,
            location_city="Coimbatore",
            location_country="India",
            location_lat=11.0168,
            location_lon=76.9558,
            timestamp=base_time
        )
        await context_engine.process_transaction(db, t1_in)

        # Step 2: Medium Transaction T2 (Coimbatore, ₹35,000, New device) -> MEDIUM
        t2_in = TransactionCreate(
            account_id=target_id,
            amount=35000.0,
            currency="INR",
            merchant_name="Reliance Digital Coimbatore",
            merchant_category="ELECTRONICS",
            transaction_type="UPI",
            bank_name="HDFC Bank",
            device_id=attack_dev,
            location_city="Coimbatore",
            location_country="India",
            location_lat=11.0168,
            location_lon=76.9558,
            timestamp=base_time + timedelta(minutes=5)
        )
        await context_engine.process_transaction(db, t2_in)

        # Step 3: High Transaction T3 (Mumbai, ₹85,000, Impossible travel + Elevated amount) -> HIGH
        t3_in = TransactionCreate(
            account_id=target_id,
            amount=85000.0,
            currency="INR",
            merchant_name="Croma Flagship Mumbai",
            merchant_category="ELECTRONICS",
            transaction_type="NET_BANKING",
            bank_name="HDFC Bank",
            device_id=attack_dev,
            location_city="Mumbai",
            location_country="India",
            location_lat=19.0760,
            location_lon=72.8777,
            timestamp=base_time + timedelta(minutes=10)
        )
        await context_engine.process_transaction(db, t3_in)

        # Step 4: Critical Transaction T4 (New Delhi, ₹1,20,000, Rapid velocity + New location) -> CRITICAL
        t4_in = TransactionCreate(
            account_id=target_id,
            amount=120000.0,
            currency="INR",
            merchant_name="Digital Gold Vault Delhi",
            merchant_category="RETAIL",
            transaction_type="IMPS",
            bank_name="HDFC Bank",
            device_id=attack_dev,
            location_city="New Delhi",
            location_country="India",
            location_lat=28.6139,
            location_lon=77.2090,
            timestamp=base_time + timedelta(minutes=12)
        )
        await context_engine.process_transaction(db, t4_in)

        # Link attack_dev to another syndicate mule account (ACC-IN-1002)
        mule_res = await db.execute(select(Account).where(Account.id == "ACC-IN-1002"))
        mule_acc = mule_res.scalar_one_or_none()
        if mule_acc:
            mule_link_res = await db.execute(select(AccountDevice).where(
                AccountDevice.account_id == "ACC-IN-1002",
                AccountDevice.device_id == attack_dev
            ))
            if not mule_link_res.scalar_one_or_none():
                db.add(AccountDevice(
                    account_id="ACC-IN-1002",
                    device_id=attack_dev,
                    first_used_at=datetime.utcnow() - timedelta(hours=1),
                    last_used_at=datetime.utcnow(),
                    usage_count=4
                ))
                await db.flush()

        # Generate and return the synthesized Investigation Dossier
        dossier = await ContextualFraudEvolutionService.analyze_account(target_id, db)
        return dossier

    @staticmethod
    async def reset_judge_demo(db: AsyncSession) -> InvestigationDossier:
        """
        Resets the Judge Demonstration Scenario for ACC-IN-1043 back to initial clean baseline state:
        - Removes all attack transactions and syndicate hardware links.
        - Seeds 1 single legitimate baseline transaction (Coimbatore, ₹2,500, UPI, LOW).
        - Returns pristine baseline Investigation Dossier.
        """
        target_id = "ACC-IN-1043"

        # Ensure account ACC-IN-1043 exists with clean status
        acc_res = await db.execute(select(Account).where(Account.id == target_id))
        target_account = acc_res.scalar_one_or_none()
        if not target_account:
            target_account = Account(
                id=target_id,
                holder_name="Tanvi Agarwal",
                email="tanvi.agarwal.1043@upi.in",
                avg_amount=2500.0,
                std_amount=450.0,
                typical_city="Coimbatore",
                typical_country="India",
                typical_location_lat=11.0168,
                typical_location_lon=76.9558,
                primary_bank="HDFC Bank",
                status="ACTIVE",
                risk_rating="LOW"
            )
            db.add(target_account)
        else:
            target_account.status = "ACTIVE"
            target_account.risk_rating = "LOW"
            target_account.typical_city = "Coimbatore"
            target_account.avg_amount = 2500.0
            target_account.std_amount = 450.0

        await db.flush()

        # 1. Clean transactions on target_id
        from sqlalchemy import delete
        await db.execute(delete(Transaction).where(Transaction.account_id == target_id))

        # 2. Remove any syndicate attack devices linked to ACC-IN-1002 or ACC-IN-1043
        await db.execute(delete(AccountDevice).where(
            AccountDevice.device_id.like("DEV-IN-ATTACK-SYNDICATE-%")
        ))
        await db.flush()

        # 3. Seed single pristine baseline transaction
        known_dev = "DEV-IN-1043-PRIM"
        base_time = datetime.utcnow() - timedelta(minutes=30)
        t1_in = TransactionCreate(
            account_id=target_id,
            amount=2500.0,
            currency="INR",
            merchant_name="A2B Sweets Coimbatore",
            merchant_category="FOOD_DELIVERY",
            transaction_type="UPI",
            bank_name="HDFC Bank",
            device_id=known_dev,
            location_city="Coimbatore",
            location_country="India",
            location_lat=11.0168,
            location_lon=76.9558,
            timestamp=base_time
        )
        await context_engine.process_transaction(db, t1_in)

        return await ContextualFraudEvolutionService.analyze_account(target_id, db)

contextual_fraud_evolution = ContextualFraudEvolutionService()

