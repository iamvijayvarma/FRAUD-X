from typing import Dict, Any, List
from app.schemas.risk import RiskAssessment, SignalEvidence

class ExplainabilityEngine:
    """Answers 'WHY WAS THIS TRANSACTION FLAGGED?' with quantified causal attribution."""

    @staticmethod
    def generate_breakdown(assessment: RiskAssessment) -> Dict[str, Any]:
        """Generates categorical point breakdown for waterfall chart rendering."""
        category_breakdown = {
            "BEHAVIORAL": 0.0,
            "DEVICE": 0.0,
            "LOCATION": 0.0,
            "VELOCITY": 0.0,
            "GRAPH": 0.0,
            "ML": 0.0
        }

        for sig in assessment.signals:
            cat = sig.category
            if cat in category_breakdown:
                category_breakdown[cat] += sig.points

        return {
            "transaction_id": assessment.transaction_id,
            "risk_score": assessment.risk_score,
            "risk_level": assessment.risk_level,
            "action": assessment.action_taken,
            "category_breakdown": category_breakdown,
            "signal_count": len(assessment.signals),
            "primary_driver": assessment.primary_reasons[0] if assessment.primary_reasons else "Normal baseline"
        }

explainability_engine = ExplainabilityEngine()
