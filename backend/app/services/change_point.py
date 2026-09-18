from typing import List, Optional
from datetime import datetime

from app.models.account import Account
from app.models.transaction import Transaction
from app.schemas.investigation import ChangePointAnalysis

class BehaviouralChangePointEngine:
    """
    Innovation 4: Behavioural Change-Point Detection
    Identifies statistical regime transitions where an account's behavioral dynamics fundamentally diverge.
    """

    @staticmethod
    def detect_change_point(account: Account, transactions: List[Transaction]) -> ChangePointAnalysis:
        hist_avg = account.avg_amount if account.avg_amount > 0 else 2500.0
        hist_city = account.typical_city or "Coimbatore"

        if not transactions or len(transactions) < 2:
            return ChangePointAnalysis(
                regime_shift_detected=False,
                change_point_timestamp=None,
                change_point_tx_id=None,
                historical_avg_amount=round(hist_avg, 2),
                historical_typical_city=hist_city,
                recent_avg_amount=round(hist_avg, 2),
                deviation_magnitude=1.0,
                affected_dimensions=[],
                narrative="Insufficient transaction sequence length to evaluate behavioral regime divergence."
            )

        chrono_txs = sorted(transactions, key=lambda t: t.timestamp)

        # Look for the transition point where behavior began deviating
        change_tx: Optional[Transaction] = None
        affected_dimensions = set()

        for i, tx in enumerate(chrono_txs):
            is_val_spike = tx.amount >= hist_avg * 3.0
            is_city_divergence = tx.location_city and tx.location_city.lower() != hist_city.lower()
            is_high_risk = tx.risk_score >= 40.0

            if (is_val_spike or is_city_divergence) and is_high_risk:
                if change_tx is None:
                    change_tx = tx

                if is_val_spike:
                    affected_dimensions.add("TRANSACTION_VALUE")
                if is_city_divergence:
                    affected_dimensions.add("LOCATION_DISPERSION")
                if tx.action_taken in ["CHALLENGE", "HOLD", "BLOCK"]:
                    affected_dimensions.add("VELOCITY_AND_AUTHORIZATION")

        # Evaluate recent window (last up to 5 transactions)
        recent_window = chrono_txs[-min(5, len(chrono_txs)):]
        recent_avg = sum(t.amount for t in recent_window) / len(recent_window)
        deviation = round(recent_avg / max(1.0, hist_avg), 1)

        regime_shift = (deviation >= 3.0 and len(affected_dimensions) >= 1) or (len(affected_dimensions) >= 2)

        if regime_shift and change_tx:
            ts_str = change_tx.timestamp.strftime("%Y-%m-%d %H:%M:%S IST")
            dims_str = ", ".join(sorted(list(affected_dimensions)))
            narrative = (
                f"Statistical regime transition detected commencing at transaction {change_tx.id} ({ts_str}). "
                f"Account departed from calibrated baseline of ₹{hist_avg:,.2f} ({hist_city}) to an active average of "
                f"₹{recent_avg:,.2f} ({deviation}x baseline shift). Compromised behavioral dimensions: [{dims_str}]."
            )
        else:
            narrative = f"Transaction behavior conforms within normal stochastic variance of baseline (₹{hist_avg:,.2f})."

        return ChangePointAnalysis(
            regime_shift_detected=regime_shift,
            change_point_timestamp=change_tx.timestamp.isoformat() if change_tx else None,
            change_point_tx_id=change_tx.id if change_tx else None,
            historical_avg_amount=round(hist_avg, 2),
            historical_typical_city=hist_city,
            recent_avg_amount=round(recent_avg, 2),
            deviation_magnitude=deviation,
            affected_dimensions=sorted(list(affected_dimensions)),
            narrative=narrative
        )

change_point_engine = BehaviouralChangePointEngine()
