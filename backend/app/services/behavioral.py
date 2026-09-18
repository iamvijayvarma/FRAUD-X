from typing import List, Optional
from datetime import datetime
from app.models.account import Account
from app.models.transaction import Transaction
from app.schemas.risk import SignalEvidence

class BehavioralEngine:
    """Evaluates spending anomalies, deviation from baseline averages, and temporal patterns in INR."""

    @staticmethod
    def evaluate(
        account: Account,
        amount: float,
        merchant_category: str,
        timestamp: datetime,
        recent_categories: List[str]
    ) -> List[SignalEvidence]:
        signals: List[SignalEvidence] = []
        
        avg = account.avg_amount or 2500.0
        std = account.std_amount or 600.0
        effective_std = max(std, 100.0)

        # 1. Z-Score Deviation
        z_score = (amount - avg) / effective_std
        multiplier = round(amount / max(avg, 1.0), 1)

        if z_score >= 6.0:
            signals.append(SignalEvidence(
                code="EXTREME_AMOUNT_OUTLIER",
                name="Extreme Spending Outlier",
                category="BEHAVIORAL",
                points=35.0,
                observed_value=f"₹{amount:,.2f} ({multiplier}x avg, Z={z_score:.1f})",
                baseline_value=f"Avg: ₹{avg:,.2f} (±₹{std:,.2f})",
                severity="CRITICAL",
                description=f"Transaction amount of ₹{amount:,.2f} is {multiplier}x higher than historical baseline of ₹{avg:,.2f} (Z-score {z_score:.1f})."
            ))
        elif z_score >= 3.0:
            signals.append(SignalEvidence(
                code="AMOUNT_ABOVE_BASELINE",
                name="Significant Spending Deviation",
                category="BEHAVIORAL",
                points=18.0,
                observed_value=f"₹{amount:,.2f} ({multiplier}x avg, Z={z_score:.1f})",
                baseline_value=f"Avg: ₹{avg:,.2f} (±₹{std:,.2f})",
                severity="WARNING",
                description=f"Transaction amount of ₹{amount:,.2f} is significantly above account normal baseline."
            ))

        # 2. Novel Merchant Category Deviation
        if recent_categories and merchant_category not in recent_categories and merchant_category in ["LUXURY", "GAMBLING", "CRYPTO_EXCHANGE"]:
            signals.append(SignalEvidence(
                code="HIGH_RISK_MERCHANT_CATEGORY",
                name="First-Time High-Risk Category",
                category="BEHAVIORAL",
                points=20.0,
                observed_value=merchant_category,
                baseline_value="Standard Retail/Grocery/UPI",
                severity="WARNING",
                description=f"Account transacting in high-risk category '{merchant_category}' for the first time."
            ))
        elif recent_categories and merchant_category not in recent_categories:
            signals.append(SignalEvidence(
                code="NEW_MERCHANT_CATEGORY",
                name="Novel Spending Category",
                category="BEHAVIORAL",
                points=10.0,
                observed_value=merchant_category,
                baseline_value="Standard categories",
                severity="INFO",
                description=f"User has no prior transaction history in '{merchant_category}'."
            ))

        # 3. Off-Hours Temporal Anomaly (e.g., 2:00 AM to 5:00 AM IST)
        hour = timestamp.hour
        if 2 <= hour <= 5:
            signals.append(SignalEvidence(
                code="OFF_HOURS_ACTIVITY",
                name="Off-Hours Transaction",
                category="BEHAVIORAL",
                points=10.0,
                observed_value=f"{hour:02d}:{timestamp.minute:02d} IST",
                baseline_value="Daytime (07:00 - 23:00)",
                severity="INFO",
                description="Transaction initiated during typical dormant sleeping hours (02:00-05:00 IST)."
            ))

        return signals

behavioral_engine = BehavioralEngine()
