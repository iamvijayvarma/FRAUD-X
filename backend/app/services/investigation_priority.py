from typing import Tuple
from app.schemas.investigation import (
    SignalConfluence,
    ChangePointAnalysis,
    CrossAccountPropagation
)

class AdaptiveInvestigationPriorityEngine:
    """
    Innovation 7: Adaptive Investigation Priority
    Computes an operational triage score to rank active cases for analysts based on multidimensional severity.
    Triage tiers: NORMAL, WATCH, INVESTIGATE, URGENT.
    """

    @staticmethod
    def calculate_priority(
        current_risk_score: float,
        is_escalating: bool,
        risk_growth_rate: float,
        confluence: SignalConfluence,
        change_point: ChangePointAnalysis,
        network: CrossAccountPropagation,
        signals_count: int
    ) -> Tuple[str, float]:
        # Weighted composite triage index
        score = 0.0

        # 1. Base current risk contribution (up to 40 pts)
        score += (current_risk_score / 100.0) * 40.0

        # 2. Risk trajectory acceleration (up to 15 pts)
        if is_escalating:
            score += 10.0
            if risk_growth_rate > 15.0:
                score += 5.0

        # 3. Multi-signal confluence synergy (up to 15 pts)
        if confluence.has_confluence:
            score += 10.0
            if confluence.confidence_score >= 0.9:
                score += 5.0

        # 4. Behavioural regime transition (up to 15 pts)
        if change_point.regime_shift_detected:
            score += 10.0
            if change_point.deviation_magnitude >= 5.0:
                score += 5.0

        # 5. Cross-account network exposure (up to 15 pts)
        if network.cluster_classification == "POTENTIAL_COORDINATED_ACTIVITY":
            score += 15.0
        elif network.cluster_classification == "HIGH_RISK_CLUSTER":
            score += 10.0
        elif network.cluster_classification == "SUSPICIOUS_CONNECTION":
            score += 5.0

        final_priority_score = round(min(100.0, max(0.0, score)), 1)

        # Classification into operational triage states
        if final_priority_score >= 75.0 or current_risk_score >= 80.0 or network.cluster_classification == "POTENTIAL_COORDINATED_ACTIVITY":
            priority_tier = "URGENT"
        elif final_priority_score >= 50.0 or current_risk_score >= 45.0 or is_escalating:
            priority_tier = "INVESTIGATE"
        elif final_priority_score >= 25.0 or signals_count > 0:
            priority_tier = "WATCH"
        else:
            priority_tier = "NORMAL"

        return priority_tier, final_priority_score

investigation_priority_engine = AdaptiveInvestigationPriorityEngine()
