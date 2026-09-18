import asyncio
from datetime import datetime, timedelta
import random
import uuid
import logging
from typing import Optional, Dict, Any, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.models.account import Account
from app.models.device import Device, AccountDevice
from app.schemas.transaction import TransactionCreate
from app.services.context_engine import context_engine
from app.websocket.connection_manager import manager
from app.utils.geo import KNOWN_CITIES

logger = logging.getLogger("fraud_x.simulator")

class AttackSimulatorService:
    """
    Real-Time Financial Fraud Attack Simulator localized to the Indian Financial Ecosystem (UPI/Cards).
    Injects 6 controlled synthetic attack scenarios and continuous streams using INR and Indian cities.
    """

    def __init__(self):
        self.is_running: bool = False
        self.current_tps: float = 1.0
        self.total_injected: int = 0
        self.active_scenario: Optional[str] = None
        self._background_task: Optional[asyncio.Task] = None

    def get_status(self) -> Dict[str, Any]:
        return {
            "is_running": self.is_running,
            "current_tps": self.current_tps,
            "total_injected": self.total_injected,
            "active_scenario": self.active_scenario,
            "status_message": f"Simulator {'active at ' + str(self.current_tps) + ' TPS' if self.is_running else 'idle (Synthetic Hackathon Data)'}."
        }

    async def trigger_scenario(self, scenario_name: str, target_account_id: Optional[str] = None) -> List[Dict[str, Any]]:
        self.active_scenario = scenario_name
        results = []

        async with AsyncSessionLocal() as db:
            if scenario_name == "ATO":
                results = await self._run_account_takeover(db, target_account_id)
            elif scenario_name == "IMPOSSIBLE_TRAVEL":
                results = await self._run_impossible_travel(db, target_account_id)
            elif scenario_name == "CARD_TESTING":
                results = await self._run_card_testing(db, target_account_id)
            elif scenario_name == "WHALE_OUTLIER":
                results = await self._run_whale_outlier(db, target_account_id)
            elif scenario_name == "MULE_RING":
                results = await self._run_mule_ring(db)
            elif scenario_name == "NORMAL_FLOW":
                results = await self._run_normal_flow(db, target_account_id)
            else:
                raise ValueError(f"Unknown scenario: {scenario_name}")

        self.active_scenario = None
        return results

    async def _run_account_takeover(self, db: AsyncSession, account_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Scenario 1: Account Takeover (ATO) - New device + ₹1,25,000 + rapid high-value transactions."""
        acc_id = account_id or "ACC-IN-1002"
        ato_device = f"DEV-IN-ATO-{uuid.uuid4().hex[:6].upper()}"
        
        txs = [
            TransactionCreate(
                account_id=acc_id,
                amount=125000.00,
                currency="INR",
                merchant_name="Croma Flagship Electronics Mumbai",
                merchant_category="ELECTRONICS",
                transaction_type="IMPS",
                bank_name="HDFC Bank",
                device_id=ato_device,
                ip_address="103.44.120.18",
                location_city="Mumbai",
                location_country="India",
                location_lat=19.0760,
                location_lon=72.8777
            ),
            TransactionCreate(
                account_id=acc_id,
                amount=95000.00,
                currency="INR",
                merchant_name="Digital Gold Hub New Delhi",
                merchant_category="CRYPTO_EXCHANGE",
                transaction_type="UPI",
                bank_name="HDFC Bank",
                device_id=ato_device,
                ip_address="103.44.120.18",
                location_city="New Delhi",
                location_country="India",
                location_lat=28.6139,
                location_lon=77.2090
            )
        ]

        results = []
        for t in txs:
            tx_obj, assessment, ai_report = await context_engine.process_transaction(db, t)
            self.total_injected += 1
            res_dict = {"tx_id": tx_obj.id, "risk_score": assessment.risk_score, "action": assessment.action_taken}
            results.append(res_dict)
            await self._broadcast_event(tx_obj, assessment, ai_report)
            await asyncio.sleep(0.4)
        return results

    async def _run_impossible_travel(self, db: AsyncSession, account_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Scenario 2: Impossible Travel (Coimbatore -> Mumbai in 5 minutes, speed > 11,000 km/h)."""
        acc_id = account_id or "ACC-IN-1005"
        device_id = f"DEV-IN-LEGIT-{uuid.uuid4().hex[:6].upper()}"
        
        # Step 1: Normal morning UPI transaction in Coimbatore
        t1 = TransactionCreate(
            account_id=acc_id,
            amount=450.00,
            currency="INR",
            merchant_name="Annapoorna Coffee Coimbatore",
            merchant_category="FOOD_DELIVERY",
            transaction_type="UPI",
            bank_name="SBI",
            device_id=device_id,
            location_city="Coimbatore",
            location_country="India",
            location_lat=11.0168,
            location_lon=76.9558,
            timestamp=datetime.utcnow() - timedelta(minutes=5)
        )
        tx1, a1, r1 = await context_engine.process_transaction(db, t1)
        self.total_injected += 1
        await self._broadcast_event(tx1, a1, r1)
        await asyncio.sleep(0.3)

        # Step 2: Transaction in Mumbai (990 km away) 5 minutes later
        t2 = TransactionCreate(
            account_id=acc_id,
            amount=48000.00,
            currency="INR",
            merchant_name="Bandra Luxury Hub Mumbai",
            merchant_category="LUXURY",
            transaction_type="Debit Card",
            bank_name="SBI",
            device_id=f"DEV-IN-MUMBAI-{uuid.uuid4().hex[:6].upper()}",
            location_city="Mumbai",
            location_country="India",
            location_lat=19.0760,
            location_lon=72.8777,
            timestamp=datetime.utcnow()
        )
        tx2, a2, r2 = await context_engine.process_transaction(db, t2)
        self.total_injected += 1
        await self._broadcast_event(tx2, a2, r2)

        return [
            {"tx_id": tx1.id, "risk_score": a1.risk_score, "action": a1.action_taken},
            {"tx_id": tx2.id, "risk_score": a2.risk_score, "action": a2.action_taken}
        ]

    async def _run_card_testing(self, db: AsyncSession, account_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Scenario 3: Rapid Automated Card / UPI Probing Sequence (7 rapid micro-transactions in seconds)."""
        acc_id = account_id or "ACC-IN-1008"
        dev_id = f"DEV-IN-BOT-{uuid.uuid4().hex[:6].upper()}"
        results = []

        amounts = [10.00, 15.00, 20.00, 35.00, 25.00, 45.00, 50.00]
        merchants = [
            ("QuickPay UPI Token", "UTILITIES"),
            ("FastRecharge VPA Test", "UTILITIES"),
            ("Online Micro Payment", "E-COMMERCE"),
            ("Gaming Credit Mini", "E-COMMERCE"),
            ("Auth Verification Service", "RETAIL"),
            ("SaaS Trial Token", "E-COMMERCE"),
            ("Micro VPA Verification", "UTILITIES")
        ]

        for i in range(len(amounts)):
            t = TransactionCreate(
                account_id=acc_id,
                amount=amounts[i],
                currency="INR",
                merchant_name=merchants[i][0],
                merchant_category=merchants[i][1],
                transaction_type="UPI",
                bank_name="ICICI Bank",
                device_id=dev_id,
                location_city="Bengaluru",
                location_country="India",
                location_lat=12.9716,
                location_lon=77.5946
            )
            tx, a, r = await context_engine.process_transaction(db, t)
            self.total_injected += 1
            results.append({"tx_id": tx.id, "risk_score": a.risk_score, "action": a.action_taken})
            await self._broadcast_event(tx, a, r)
            await asyncio.sleep(0.15)
        return results

    async def _run_whale_outlier(self, db: AsyncSession, account_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Scenario 4: Whale Outlier - ₹4,80,000 for account with ₹2,500 average baseline."""
        acc_id = account_id or "ACC-IN-1015"
        dev_id = f"DEV-IN-WHALE-{uuid.uuid4().hex[:6].upper()}"

        t = TransactionCreate(
            account_id=acc_id,
            amount=480000.00,
            currency="INR",
            merchant_name="Tanishq Jewellery Mumbai",
            merchant_category="LUXURY",
            transaction_type="Net Banking",
            bank_name="Axis Bank",
            device_id=dev_id,
            location_city="Mumbai",
            location_country="India",
            location_lat=19.0760,
            location_lon=72.8777
        )
        tx, a, r = await context_engine.process_transaction(db, t)
        self.total_injected += 1
        await self._broadcast_event(tx, a, r)
        return [{"tx_id": tx.id, "risk_score": a.risk_score, "action": a.action_taken}]

    async def _run_mule_ring(self, db: AsyncSession) -> List[Dict[str, Any]]:
        """Scenario 5: Coordinated Mule Syndicate - 4 Indian accounts, 1 shared device, circular transfer loop."""
        mule_device = "DEV-IN-MULE-SHARED-01"
        accounts = ["ACC-IN-1030", "ACC-IN-1031", "ACC-IN-1032", "ACC-IN-1033"]
        results = []

        # Circular chain: ACC-IN-1030 -> ACC-IN-1031 -> ACC-IN-1032 -> ACC-IN-1033 -> ACC-IN-1030
        transfers = [
            (accounts[0], accounts[1], 145000.00),
            (accounts[1], accounts[2], 140000.00),
            (accounts[2], accounts[3], 135000.00),
            (accounts[3], accounts[0], 130000.00)
        ]

        for src, dst, amt in transfers:
            t = TransactionCreate(
                account_id=src,
                target_account_id=dst,
                amount=amt,
                currency="INR",
                transaction_type="IMPS",
                bank_name="Kotak Mahindra Bank",
                merchant_name=f"IMPS P2P Transfer to {dst}",
                merchant_category="TRANSFER",
                device_id=mule_device,
                location_city="Hyderabad",
                location_country="India",
                location_lat=17.3850,
                location_lon=78.4867
            )
            tx, a, r = await context_engine.process_transaction(db, t)
            self.total_injected += 1
            results.append({"tx_id": tx.id, "risk_score": a.risk_score, "action": a.action_taken})
            await self._broadcast_event(tx, a, r)
            await asyncio.sleep(0.3)
        return results

    async def _run_normal_flow(self, db: AsyncSession, account_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Scenario 6: Legitimate High-Volume Indian Shopping (UPI / Swiggy / DMart)."""
        acc_id = account_id or f"ACC-IN-{random.randint(1001, 1025)}"
        
        res = await db.execute(select(Account).where(Account.id == acc_id))
        acc = res.scalar_one_or_none()
        
        city = acc.typical_city if acc else "Bengaluru"
        lat = acc.typical_location_lat if acc else 12.9716
        lon = acc.typical_location_lon if acc else 77.5946
        bank = acc.primary_bank if acc and acc.primary_bank else "HDFC Bank"
        amt = round(random.gauss(acc.avg_amount, acc.std_amount * 0.4), 2) if acc else 1450.00
        amt = max(100.0, amt)

        dev_res = await db.execute(select(AccountDevice.device_id).where(AccountDevice.account_id == acc_id))
        dev_id = dev_res.scalars().first() or f"DEV-IN-PRIM-{uuid.uuid4().hex[:6]}"

        merchants = [
            ("Swiggy Online", "FOOD_DELIVERY", "UPI"),
            ("DMart Supermarket", "GROCERY", "UPI"),
            ("Flipkart Retail", "E-COMMERCE", "UPI"),
            ("Indian Oil Petrol Pump", "FUEL", "POS"),
            ("BigBasket", "GROCERY", "UPI")
        ]
        m_name, m_cat, m_type = random.choice(merchants)

        t = TransactionCreate(
            account_id=acc_id,
            amount=amt,
            currency="INR",
            merchant_name=m_name,
            merchant_category=m_cat,
            transaction_type=m_type,
            bank_name=bank,
            device_id=dev_id,
            location_city=city,
            location_country="India",
            location_lat=lat + random.uniform(-0.01, 0.01),
            location_lon=lon + random.uniform(-0.01, 0.01)
        )
        tx, a, r = await context_engine.process_transaction(db, t)
        self.total_injected += 1
        await self._broadcast_event(tx, a, r)
        return [{"tx_id": tx.id, "risk_score": a.risk_score, "action": a.action_taken}]

    async def start_stream(self, tps: float = 1.0):
        if self.is_running:
            return
        self.is_running = True
        self.current_tps = max(0.2, min(20.0, tps))
        self._background_task = asyncio.create_task(self._stream_loop())
        logger.info(f"Simulator stream active at {self.current_tps} TPS (INR / India context).")

    async def stop_stream(self):
        self.is_running = False
        if self._background_task:
            self._background_task.cancel()
            self._background_task = None
        logger.info("Simulator stream halted.")

    async def _stream_loop(self):
        while self.is_running:
            try:
                interval = 1.0 / self.current_tps
                roll = random.random()
                async with AsyncSessionLocal() as db:
                    if roll < 0.85:
                        await self._run_normal_flow(db)
                    elif roll < 0.90:
                        await self._run_impossible_travel(db)
                    elif roll < 0.95:
                        await self._run_whale_outlier(db)
                    else:
                        await self._run_account_takeover(db)
                await asyncio.sleep(interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in simulator loop: {e}")
                await asyncio.sleep(1.0)

    async def _broadcast_event(self, tx, assessment, ai_report):
        event_payload = {
            "id": tx.id,
            "timestamp": tx.timestamp.isoformat(),
            "account_id": tx.account_id,
            "target_account_id": tx.target_account_id,
            "amount": tx.amount,
            "currency": tx.currency,
            "merchant_name": tx.merchant_name,
            "merchant_category": tx.merchant_category,
            "transaction_type": tx.transaction_type,
            "bank_name": getattr(tx, 'bank_name', 'HDFC Bank'),
            "device_id": tx.device_id,
            "location_city": tx.location_city,
            "location_country": tx.location_country,
            "location_lat": tx.location_lat,
            "location_lon": tx.location_lon,
            "risk_score": assessment.risk_score,
            "risk_level": assessment.risk_level,
            "action_taken": assessment.action_taken,
            "assessment": assessment.model_dump(),
            "ai_narrative": ai_report.model_dump()
        }
        await manager.broadcast("TX_PROCESSED", event_payload)

        if assessment.risk_level in ["HIGH", "CRITICAL"]:
            await manager.broadcast("ALERT_RAISED", {
                "transaction_id": tx.id,
                "account_id": tx.account_id,
                "risk_score": assessment.risk_score,
                "risk_level": assessment.risk_level,
                "summary": assessment.primary_reasons[0] if assessment.primary_reasons else "High Risk UPI/Banking Activity",
                "timestamp": tx.timestamp.isoformat()
            })

simulator_service = AttackSimulatorService()
