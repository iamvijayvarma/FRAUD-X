from typing import List
from datetime import datetime
import json

from app.models.transaction import Transaction
from app.schemas.investigation import RiskEvolutionTrajectory, RiskTrajectoryPoint

class TemporalRiskEvolutionEngine:
    """
    Innovation 1: Temporal Risk Evolution
    Evaluates risk trajectories across sequences of transactions rather than treating events in isolation.
    """

    @staticmethod
    def analyze_trajectory(account_id: str, transactions: List[Transaction]) -> RiskEvolutionTrajectory:
        if not transactions:
            return RiskEvolutionTrajectory(
                account_id=account_id,
                trajectory_levels=["LOW"],
                score_history=[0.0],
                is_escalating=False,
                risk_growth_rate=0.0,
                accumulated_signals=[],
                escalation_points_count=0,
                avg_interval_seconds=0.0,
                timeline_points=[]
            )

        # Sort chronological (oldest to newest)
        chrono_txs = sorted(transactions, key=lambda t: t.timestamp)

        timeline_points: List[RiskTrajectoryPoint] = []
        scores: List[float] = []
        levels: List[str] = []
        all_signals_set = set()

        prev_time = None
        intervals = []
        escalation_count = 0
        prev_level_idx = 0

        LEVEL_RANKS = {"LOW": 0, "MEDIUM": 1, "HIGH": 2, "CRITICAL": 3}

        for i, tx in enumerate(chrono_txs):
            # Parse signals from evidence_json or assessment
            signals_list = []
            if tx.evidence_json:
                try:
                    data = json.loads(tx.evidence_json)
                    signals_list = [s.get("code", "") for s in data.get("signals", []) if s.get("code")]
                except Exception:
                    pass

            for sig in signals_list:
                all_signals_set.add(sig)

            scores.append(round(tx.risk_score, 1))
            levels.append(tx.risk_level)

            cur_level_idx = LEVEL_RANKS.get(tx.risk_level, 0)
            if i > 0 and cur_level_idx > prev_level_idx:
                escalation_count += 1
            prev_level_idx = cur_level_idx

            if prev_time is not None:
                delta_sec = (tx.timestamp - prev_time).total_seconds()
                if delta_sec > 0:
                    intervals.append(delta_sec)
            prev_time = tx.timestamp

            timeline_points.append(RiskTrajectoryPoint(
                transaction_id=tx.id,
                timestamp=tx.timestamp.isoformat(),
                amount=round(tx.amount, 2),
                currency=tx.currency or "INR",
                city=tx.location_city or "Unknown",
                risk_score=round(tx.risk_score, 1),
                risk_level=tx.risk_level,
                action_taken=tx.action_taken,
                signals=signals_list,
                device_id=tx.device_id or "UNKNOWN",
                is_new_device="NEW_DEVICE_DETECTED" in signals_list
            ))

        # Determine growth rate and escalation trend
        if len(scores) >= 2:
            first_half_avg = sum(scores[:len(scores)//2]) / max(1, len(scores)//2)
            second_half_avg = sum(scores[len(scores)//2:]) / max(1, len(scores) - len(scores)//2)
            risk_growth_rate = round((scores[-1] - scores[0]) / max(1, len(scores) - 1), 2)
            is_escalating = (second_half_avg > first_half_avg + 5.0) or (scores[-1] >= 60.0 and scores[-1] > scores[0])
        else:
            risk_growth_rate = 0.0
            is_escalating = scores[0] >= 60.0

        avg_interval = round(sum(intervals) / len(intervals), 1) if intervals else None

        return RiskEvolutionTrajectory(
            account_id=account_id,
            trajectory_levels=levels,
            score_history=scores,
            is_escalating=is_escalating,
            risk_growth_rate=risk_growth_rate,
            accumulated_signals=sorted(list(all_signals_set)),
            escalation_points_count=escalation_count,
            avg_interval_seconds=avg_interval,
            timeline_points=timeline_points
        )

risk_evolution_engine = TemporalRiskEvolutionEngine()
