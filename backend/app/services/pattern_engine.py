from typing import List
from app.schemas.investigation import (
    FraudPatternHypothesis,
    RiskEvolutionTrajectory,
    SignalConfluence,
    ChangePointAnalysis,
    CrossAccountPropagation
)

class FraudPatternFormationEngine:
    """
    Innovation 5: Fraud Pattern Formation
    Synthesizes signals, temporal trajectories, and network linkages into human-readable investigation hypotheses.
    """

    @staticmethod
    def synthesize_patterns(
        evolution: RiskEvolutionTrajectory,
        confluence: SignalConfluence,
        change_point: ChangePointAnalysis,
        network: CrossAccountPropagation
    ) -> List[FraudPatternHypothesis]:
        hypotheses: List[FraudPatternHypothesis] = []
        sig_set = set(evolution.accumulated_signals)

        # 1. Account Takeover (ATO) Pattern
        if (
            ("NEW_DEVICE_DETECTED" in sig_set or "DEV-IN-" in str(sig_set)) and
            change_point.regime_shift_detected and
            ("EXTREME_AMOUNT_OUTLIER" in sig_set or change_point.deviation_magnitude >= 3.0)
        ):
            evidence = [
                "Novel hardware fingerprint introduced to account",
                f"Statistical regime change of {change_point.deviation_magnitude}x baseline spend",
                "Rapid escalation from baseline to elevated risk state",
                f"Multi-vector signal confluence: {confluence.confluence_name}"
            ]
            if "IMPOSSIBLE_TRAVEL_VELOCITY" in sig_set:
                evidence.append("Immediate geographic translocation across state boundaries")

            hypotheses.append(FraudPatternHypothesis(
                pattern_id="PAT-ATO-01",
                pattern_name="Account Takeover (ATO) Pattern",
                pattern_type="CREDENTIAL_COMPROMISE_HYPOTHESIS",
                confidence_score=0.93,
                primary_evidence=evidence,
                investigative_hypothesis=(
                    "Behavioral pattern is consistent with credential theft or session hijacking. "
                    "An unauthenticated hardware environment initiated high-value out-of-character disbursements "
                    "shortly after initial authentication."
                )
            ))

        # 2. Impossible Travel Velocity Pattern
        if "IMPOSSIBLE_TRAVEL_VELOCITY" in sig_set:
            evidence = [
                "Geodesic movement speed exceeds commercial aeronautical limits (>800 km/h)",
                "Physical presence impossible within elapsed transaction interval",
                "Indicates proxy manipulation, session cloning, or multi-party credential sharing"
            ]
            hypotheses.append(FraudPatternHypothesis(
                pattern_id="PAT-GEO-02",
                pattern_name="Impossible Travel Teleportation",
                pattern_type="GEOGRAPHIC_DIVERGENCE_HYPOTHESIS",
                confidence_score=0.96,
                primary_evidence=evidence,
                investigative_hypothesis=(
                    "Physical spatial constraints violated across consecutive events. Strong hypothesis of "
                    "session sharing, automated bot proxying, or simultaneous exploitation across geographic hubs."
                )
            ))

        # 3. Coordinated Network Syndicate Pattern
        if (
            network.cluster_classification in ["POTENTIAL_COORDINATED_ACTIVITY", "HIGH_RISK_CLUSTER"] or
            "SUSPICIOUS_DEVICE_REUSE" in sig_set or
            "CIRCULAR_TRANSFER_RING" in sig_set
        ):
            evidence = [
                f"Hardware fingerprint linked across {network.correlated_accounts_count} distinct customer accounts",
                f"Network cluster classified as: {network.cluster_classification}",
                f"Network exposure score: {network.network_exposure_score:.0f}/100"
            ]
            if "CIRCULAR_TRANSFER_RING" in sig_set:
                evidence.append("Closed cyclical fund flow detected (Layering topology)")

            hypotheses.append(FraudPatternHypothesis(
                pattern_id="PAT-NET-03",
                pattern_name="Coordinated Network Syndicate",
                pattern_type="MULE_RING_HYPOTHESIS",
                confidence_score=0.91,
                primary_evidence=evidence,
                investigative_hypothesis=(
                    "Entity connections demonstrate centralized infrastructure reuse across nominally unrelated customer accounts. "
                    "Consistent with professional mule syndicates or organized fraud rings."
                )
            ))

        # 4. Automated Card Testing / UPI Brute-Force Pattern
        if "CARD_TESTING_FREQUENCY" in sig_set or (evolution.avg_interval_seconds and evolution.avg_interval_seconds < 3.0 and len(evolution.timeline_points) >= 4):
            evidence = [
                "High-frequency sub-second authorization attempts",
                "Successive micro-value transactions",
                "Automated scripting cadence departing from human interaction speeds"
            ]
            hypotheses.append(FraudPatternHypothesis(
                pattern_id="PAT-BOT-04",
                pattern_name="Automated Card Testing / Rapid Velocity",
                pattern_type="SCRIPTED_PROBING_HYPOTHESIS",
                confidence_score=0.89,
                primary_evidence=evidence,
                investigative_hypothesis=(
                    "Sub-second authorization bursts suggest automated payment gateway probing. "
                    "High probability of programmatic card testing or bot-assisted VPA enumeration."
                )
            ))

        # 5. Whale Outlier Capital Extraction Pattern
        if "EXTREME_AMOUNT_OUTLIER" in sig_set and not any(h.pattern_id == "PAT-ATO-01" for h in hypotheses):
            evidence = [
                "Transaction amount severely exceeds historical spending distribution",
                "Extreme statistical Z-score deviation",
                "Sudden liquidity extraction"
            ]
            hypotheses.append(FraudPatternHypothesis(
                pattern_id="PAT-OUTLIER-05",
                pattern_name="Whale Spend Liquidity Extraction",
                pattern_type="ANOMALOUS_VALUE_HYPOTHESIS",
                confidence_score=0.85,
                primary_evidence=evidence,
                investigative_hypothesis=(
                    "Isolated or rapid high-value transactions disproportionate to historical average. "
                    "Warrants verification of beneficiary intent and authentication step-up."
                )
            ))

        # Fallback: Baseline Conformance
        if not hypotheses:
            hypotheses.append(FraudPatternHypothesis(
                pattern_id="PAT-NORM-00",
                pattern_name="Normal Baseline Conformance",
                pattern_type="LEGITIMATE_BEHAVIOURAL_PROFILE",
                confidence_score=0.95,
                primary_evidence=[
                    "Spending values conform with historical calibrated mean (µ)",
                    "Transactions originate from authenticated hardware bindings",
                    "Geographic continuity preserved within home jurisdiction"
                ],
                investigative_hypothesis=(
                    "Transaction sequence demonstrates normal customer behavioral fidelity. "
                    "No anomalous multi-vector escalation detected."
                )
            ))

        return hypotheses

pattern_engine = FraudPatternFormationEngine()
