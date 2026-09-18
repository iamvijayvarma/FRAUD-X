from typing import List, Optional
from app.models.account import Account
from app.models.transaction import Transaction
from app.schemas.investigation import (
    ExplainableFraudStory,
    RiskEvolutionTrajectory,
    SignalConfluence,
    ChangePointAnalysis,
    CrossAccountPropagation,
    FraudPatternHypothesis
)

class ExplainableFraudStoryEngine:
    """
    Innovation 6: Explainable Fraud Story
    Synthesizes the end-to-end evolutionary narrative across a 7-stage causal framework:
    TIMELINE -> BEHAVIOUR CHANGE -> SIGNAL CONFLUENCE -> NETWORK RELATIONSHIP -> RISK ESCALATION -> CURRENT ASSESSMENT -> RECOMMENDED ACTION.
    """

    @staticmethod
    def generate_story(
        account: Account,
        evolution: RiskEvolutionTrajectory,
        confluence: SignalConfluence,
        change_point: ChangePointAnalysis,
        network: CrossAccountPropagation,
        patterns: List[FraudPatternHypothesis],
        latest_tx: Optional[Transaction]
    ) -> ExplainableFraudStory:
        acc_id = account.id
        holder = account.holder_name
        bank = account.primary_bank or "HDFC Bank"
        home_city = account.typical_city or "Coimbatore"
        baseline_amt = account.avg_amount

        # 1. Timeline
        if len(evolution.timeline_points) >= 2:
            first_pt = evolution.timeline_points[0]
            last_pt = evolution.timeline_points[-1]
            cities_visited = list(dict.fromkeys(pt.city for pt in evolution.timeline_points if pt.city))
            cities_str = " -> ".join(cities_visited) if len(cities_visited) > 1 else home_city

            timeline_desc = (
                f"Activity began with historical transactions in {home_city}. "
                f"Across {len(evolution.timeline_points)} monitored events, activity traversed [{cities_str}]. "
                f"Final transaction recorded at {last_pt.timestamp}."
            )
        else:
            timeline_desc = f"Account maintains localized transactional history in {home_city}."

        # 2. Behaviour Change
        if change_point.regime_shift_detected:
            behaviour_change_desc = (
                f"Account departed from calibrated baseline of ₹{baseline_amt:,.2f} ({home_city}) "
                f"to an active burst averaging ₹{change_point.recent_avg_amount:,.2f} "
                f"({change_point.deviation_magnitude}x baseline shift). "
                f"Divergence detected across: {', '.join(change_point.affected_dimensions)}."
            )
        else:
            behaviour_change_desc = (
                f"Account spending is consistent with calibrated baseline (₹{baseline_amt:,.2f}, {home_city}). "
                "No statistical regime divergence identified."
            )

        # 3. Signal Confluence
        if confluence.has_confluence:
            signal_confluence_desc = (
                f"Signal Confluence Engine identified synergistic co-occurrence of: "
                f"[{', '.join(confluence.contributing_signals)}]. "
                f"Confluence cluster classified as '{confluence.confluence_name}' with a {confluence.compounding_multiplier}x "
                f"compounding risk multiplier (+{confluence.combined_risk_boost:.0f} points)."
            )
        else:
            signal_confluence_desc = "Observed indicators appeared as isolated independent signals without multi-vector confluence."

        # 4. Network Relationship
        if network.cluster_classification != "NORMAL":
            network_relationship_desc = (
                f"Cross-account entity propagation links account {acc_id} with {network.correlated_accounts_count} "
                f"other account(s). Classification: '{network.cluster_classification}'. "
                f"Hardware fingerprint(s) [{', '.join(d[:12] + '...' for d in network.shared_devices)}] "
                "exhibit multi-account reuse typical of organized mule syndicates."
            )
        else:
            network_relationship_desc = (
                f"No unauthorized device sharing or cross-account entanglement identified. "
                "Hardware fingerprint is uniquely bound to this customer entity."
            )

        # 5. Risk Escalation
        trajectory_str = " -> ".join(evolution.trajectory_levels)
        if evolution.is_escalating:
            risk_escalation_desc = (
                f"Progressive risk escalation detected: [{trajectory_str}]. "
                f"Risk score accelerated at {evolution.risk_growth_rate:+.1f} points/transaction "
                f"across {evolution.escalation_points_count} escalation boundaries."
            )
        else:
            risk_escalation_desc = f"Risk trajectory is stable: [{trajectory_str}]. Score variance is minimal."

        # 6. Current Assessment
        primary_pattern = patterns[0].pattern_name if patterns else "Unspecified Pattern"
        curr_score = evolution.score_history[-1] if evolution.score_history else 0.0
        curr_level = evolution.trajectory_levels[-1] if evolution.trajectory_levels else "LOW"

        current_assessment_desc = (
            f"Current risk posture is {curr_level} ({curr_score:.1f}/100). "
            f"Primary investigative hypothesis: '{primary_pattern}'. "
            f"{patterns[0].investigative_hypothesis if patterns else ''}"
        )

        # 7. Recommended Action
        if curr_score >= 80.0:
            recommended_action_desc = (
                f"BLOCK & FREEZE: Immediately freeze outbound UPI and IMPS transfer capabilities for {acc_id}. "
                "Quarantine linked device hardware fingerprints across core banking gateways. "
                "Initiate emergency customer callback to verified registered mobile number."
            )
        elif curr_score >= 50.0:
            recommended_action_desc = (
                f"HOLD & STEP-UP: Place outbound transactions on 15-minute hold pending mandatory Step-Up biometric/OTP 2FA. "
                "Notify security operations to review device integrity."
            )
        else:
            recommended_action_desc = "ALLOW & MONITOR: Continue automated passive monitoring. No manual intervention required."

        # Full Synthesized Narrative
        full_narrative = (
            f"Account {acc_id} ({holder}, {bank}) established an operational baseline in {home_city} with an expected "
            f"spending mean of ₹{baseline_amt:,.2f}. {timeline_desc} {behaviour_change_desc} {signal_confluence_desc} "
            f"{network_relationship_desc} As a result, the account experienced a {risk_escalation_desc} "
            f"Overall diagnostic: {current_assessment_desc} Action verdict: {recommended_action_desc}"
        )

        return ExplainableFraudStory(
            timeline=timeline_desc,
            behaviour_change=behaviour_change_desc,
            signal_confluence=signal_confluence_desc,
            network_relationship=network_relationship_desc,
            risk_escalation=risk_escalation_desc,
            current_assessment=current_assessment_desc,
            recommended_action=recommended_action_desc,
            full_narrative=full_narrative
        )

fraud_story_engine = ExplainableFraudStoryEngine()
