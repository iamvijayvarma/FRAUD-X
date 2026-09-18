from typing import List, Set, Optional
from app.schemas.investigation import SignalConfluence
from app.schemas.risk import SignalEvidence

class SignalConfluenceEngine:
    """
    Innovation 2: Signal Confluence Engine
    Detects non-linear risk compounding when multiple weak/medium signals appear together.
    """

    @staticmethod
    def evaluate(signals: List[str]) -> SignalConfluence:
        sig_set: Set[str] = set(signals)

        # 1. Account Takeover Cluster: Hardware Novelty + Geodesic Shift + Amount Outlier + Velocity
        ato_elements = {"NEW_DEVICE_DETECTED", "IMPOSSIBLE_TRAVEL_VELOCITY", "EXTREME_AMOUNT_OUTLIER", "AMOUNT_ABOVE_BASELINE", "RAPID_BURST_VELOCITY", "HOURLY_VOLUME_SPIKE"}
        ato_matches = sig_set.intersection(ato_elements)

        if "NEW_DEVICE_DETECTED" in sig_set and len(ato_matches) >= 3:
            return SignalConfluence(
                has_confluence=True,
                confluence_name="ACCOUNT_TAKEOVER_CONFLUENCE",
                compounding_multiplier=1.65,
                combined_risk_boost=35.0,
                contributing_signals=sorted(list(ato_matches)),
                confidence_score=0.94,
                description="High-confidence convergence of novel unauthenticated hardware, geographic shift, and rapid elevated capital extraction."
            )

        # 2. Syndicate Mule Ring Cluster: Shared Hardware + Cyclical Flow + Velocity
        syndicate_elements = {"SUSPICIOUS_DEVICE_REUSE", "CIRCULAR_TRANSFER_RING", "RAPID_BURST_VELOCITY", "UNSUPERVISED_ML_OUTLIER"}
        syndicate_matches = sig_set.intersection(syndicate_elements)
        if len(syndicate_matches) >= 2 and ("SUSPICIOUS_DEVICE_REUSE" in sig_set or "CIRCULAR_TRANSFER_RING" in sig_set):
            return SignalConfluence(
                has_confluence=True,
                confluence_name="SYNDICATE_MULE_RING_CONFLUENCE",
                compounding_multiplier=1.75,
                combined_risk_boost=40.0,
                contributing_signals=sorted(list(syndicate_matches)),
                confidence_score=0.96,
                description="Cross-entity hardware entanglement coupled with rapid sequential transfers indicates organized money mule layering."
            )

        # 3. Impossible Travel + Device Hijack Cluster
        if "IMPOSSIBLE_TRAVEL_VELOCITY" in sig_set and "NEW_DEVICE_DETECTED" in sig_set:
            return SignalConfluence(
                has_confluence=True,
                confluence_name="GEO_DEVICE_HIJACK_CONFLUENCE",
                compounding_multiplier=1.50,
                combined_risk_boost=30.0,
                contributing_signals=["IMPOSSIBLE_TRAVEL_VELOCITY", "NEW_DEVICE_DETECTED"],
                confidence_score=0.91,
                description="Simultaneous emergence of an unregistered hardware profile at a physically inaccessible geodesic location."
            )

        # 4. Automated Bot / Card Testing Cluster
        testing_elements = {"CARD_TESTING_FREQUENCY", "RAPID_BURST_VELOCITY", "NEW_DEVICE_DETECTED"}
        testing_matches = sig_set.intersection(testing_elements)
        if len(testing_matches) >= 2 and ("CARD_TESTING_FREQUENCY" in sig_set or "RAPID_BURST_VELOCITY" in sig_set):
            return SignalConfluence(
                has_confluence=True,
                confluence_name="AUTOMATED_CARD_TESTING_CONFLUENCE",
                compounding_multiplier=1.40,
                combined_risk_boost=25.0,
                contributing_signals=sorted(list(testing_matches)),
                confidence_score=0.88,
                description="High-frequency sequential authorizations testing payment instrument validity via automated scripting."
            )

        # 5. Behavioral Shift: Novel Category + Moderate Spike
        if "NEW_MERCHANT_CATEGORY" in sig_set and ("AMOUNT_ABOVE_BASELINE" in sig_set or "EXTREME_AMOUNT_OUTLIER" in sig_set):
            return SignalConfluence(
                has_confluence=True,
                confluence_name="BEHAVIORAL_DIVERGENCE_CONFLUENCE",
                compounding_multiplier=1.25,
                combined_risk_boost=15.0,
                contributing_signals=sorted(list(sig_set.intersection({"NEW_MERCHANT_CATEGORY", "AMOUNT_ABOVE_BASELINE", "EXTREME_AMOUNT_OUTLIER"}))),
                confidence_score=0.78,
                description="Concurrent departure from typical spending categories and spending volume thresholds."
            )

        # Fallback: Single or No Confluence
        return SignalConfluence(
            has_confluence=False,
            confluence_name="ISOLATED_EVIDENCE_SIGNALS",
            compounding_multiplier=1.0,
            combined_risk_boost=0.0,
            contributing_signals=sorted(list(sig_set)),
            confidence_score=0.50,
            description="Detected signals do not meet multi-vector confluence thresholds; evaluated linearly."
        )

signal_confluence_engine = SignalConfluenceEngine()
