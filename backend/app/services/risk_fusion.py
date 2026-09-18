from typing import List, Tuple
from app.schemas.risk import SignalEvidence, RiskAssessment
from app.config import settings

class RiskFusionEngine:
    """Synthesizes multi-engine signals, enforces override safety rules, and generates decision."""

    @staticmethod
    def fuse(
        transaction_id: str,
        signals: List[SignalEvidence],
        ml_score: float,
        speed_kmh: float | None = None,
        dist_km: float | None = None,
        count_1m: int = 1,
        count_5m: int = 1,
        share_count: int = 1,
        is_circular: bool = False
    ) -> RiskAssessment:
        # Sum of raw points
        raw_score = sum(s.points for s in signals)
        
        # Signal codes set for fast override checks
        signal_codes = {s.code for s in signals}

        # Safety override rules (Hard Gates)
        if "IMPOSSIBLE_TRAVEL_VELOCITY" in signal_codes:
            raw_score = max(raw_score, 80.0)

        if "SUSPICIOUS_DEVICE_REUSE" in signal_codes and "RAPID_BURST_VELOCITY" in signal_codes:
            raw_score = max(raw_score, 92.0)

        if "CIRCULAR_TRANSFER_RING" in signal_codes:
            raw_score = max(raw_score, 88.0)

        if "EXTREME_AMOUNT_OUTLIER" in signal_codes and "NEW_DEVICE_DETECTED" in signal_codes:
            raw_score = max(raw_score, 85.0)

        # Normalized clamped score
        final_score = round(min(100.0, max(0.0, raw_score)), 1)

        # Risk Tier Classification
        if final_score >= settings.RISK_THRESHOLD_HIGH:
            risk_level = "CRITICAL"
            action = "BLOCK"
        elif final_score >= settings.RISK_THRESHOLD_MEDIUM:
            risk_level = "HIGH"
            action = "HOLD"
        elif final_score >= settings.RISK_THRESHOLD_LOW:
            risk_level = "MEDIUM"
            action = "CHALLENGE" if final_score >= 45.0 else "MONITOR"
        else:
            risk_level = "LOW"
            action = "ALLOW"

        # Primary Reasons for Explainability
        # Sort signals by points descending
        sorted_signals = sorted(signals, key=lambda s: s.points, reverse=True)
        primary_reasons = [s.description for s in sorted_signals[:3]]
        if not primary_reasons:
            primary_reasons = ["Transaction metrics align with historical account profile and expected behavior."]

        return RiskAssessment(
            transaction_id=transaction_id,
            risk_score=final_score,
            risk_level=risk_level,
            action_taken=action,
            primary_reasons=primary_reasons,
            signals=signals,
            ml_score=ml_score,
            velocity_count_1m=count_1m,
            velocity_count_5m=count_5m,
            speed_kmh=speed_kmh,
            distance_km=dist_km,
            device_account_count=share_count,
            is_circular_loop=is_circular
        )

risk_fusion = RiskFusionEngine()
