from typing import List, Tuple
from datetime import datetime, timedelta
from app.models.transaction import Transaction
from app.schemas.risk import SignalEvidence
from app.config import settings

class VelocityEngine:
    """Evaluates multi-window transaction velocity, frequency bursts, and rapid card/UPI testing patterns."""

    @staticmethod
    def evaluate(
        current_time: datetime,
        current_amount: float,
        recent_transactions: List[Transaction]
    ) -> Tuple[List[SignalEvidence], int, int]:
        signals: List[SignalEvidence] = []

        window_1m = current_time - timedelta(seconds=settings.BURST_WINDOW_SECONDS)
        window_5m = current_time - timedelta(seconds=settings.CARD_TESTING_WINDOW_SECONDS)
        window_1h = current_time - timedelta(hours=1)

        # Count recent transactions within sliding windows
        tx_last_1m = [tx for tx in recent_transactions if tx.timestamp >= window_1m]
        tx_last_5m = [tx for tx in recent_transactions if tx.timestamp >= window_5m]
        tx_last_1h = [tx for tx in recent_transactions if tx.timestamp >= window_1h]

        count_1m = len(tx_last_1m) + 1 # include current transaction
        count_5m = len(tx_last_5m) + 1

        # 1. Rapid Burst Velocity (e.g. >= 4 tx in 60s)
        if count_1m >= settings.BURST_THRESHOLD_COUNT:
            signals.append(SignalEvidence(
                code="RAPID_BURST_VELOCITY",
                name="Rapid Transaction Burst",
                category="VELOCITY",
                points=35.0,
                observed_value=f"{count_1m} transactions in 60 seconds",
                baseline_value="Max 1 tx per 5 minutes",
                severity="CRITICAL",
                description=f"Abnormal burst of {count_1m} transactions detected within a 60-second window, characteristic of an automated script or bot attack."
            ))

        # 2. Card/UPI Testing Frequency Pattern (e.g. >= 7 tx in 5m)
        if count_5m >= settings.CARD_TESTING_THRESHOLD_COUNT:
            signals.append(SignalEvidence(
                code="CARD_TESTING_FREQUENCY",
                name="Automated Probing Sequence",
                category="VELOCITY",
                points=40.0,
                observed_value=f"{count_5m} transactions in 5 minutes",
                baseline_value="Max 2 tx per 5 minutes",
                severity="CRITICAL",
                description=f"High frequency of {count_5m} rapid consecutive attempts matching automated card validity or UPI VPA probe signatures."
            ))

        # 3. Hourly Spend Surge (Threshold adapted for INR: ₹1,50,000)
        hourly_total = sum(tx.amount for tx in tx_last_1h) + current_amount
        if len(tx_last_1h) >= 3 and hourly_total > 150000.0:
            signals.append(SignalEvidence(
                code="HOURLY_VOLUME_SPIKE",
                name="Hourly Cumulative Volume Surge",
                category="VELOCITY",
                points=25.0,
                observed_value=f"₹{hourly_total:,.2f} in 1 hour",
                baseline_value="Standard daily velocity",
                severity="WARNING",
                description=f"Aggregated spending reached ₹{hourly_total:,.2f} within the last hour across multiple transactions."
            ))

        return signals, count_1m, count_5m

velocity_engine = VelocityEngine()
