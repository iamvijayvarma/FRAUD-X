import pytest
from httpx import AsyncClient, ASGITransport
from datetime import datetime, timedelta

from app.main import app
from app.models.account import Account
from app.models.transaction import Transaction
from app.services.risk_evolution import risk_evolution_engine
from app.services.signal_confluence import signal_confluence_engine
from app.services.change_point import change_point_engine
from app.services.cross_account_propagation import cross_account_propagation_engine
from app.services.pattern_engine import pattern_engine
from app.services.fraud_story import fraud_story_engine
from app.services.investigation_priority import investigation_priority_engine
from app.services.contextual_fusion import contextual_fraud_evolution

def create_mock_tx(tx_id: str, amount: float, minutes_ago: int, risk_score: float, risk_level: str, city: str, signals: list, device_id: str = "DEV-01") -> Transaction:
    import json
    tx = Transaction(
        id=tx_id,
        account_id="ACC-IN-TEST",
        amount=amount,
        currency="INR",
        timestamp=datetime.utcnow() - timedelta(minutes=minutes_ago),
        location_city=city,
        location_lat=11.0168,
        location_lon=76.9558,
        device_id=device_id,
        transaction_type="UPI",
        merchant_category="GROCERY",
        risk_score=risk_score,
        risk_level=risk_level,
        action_taken="ALLOW" if risk_level == "LOW" else ("CHALLENGE" if risk_level == "MEDIUM" else "BLOCK"),
        evidence_json=json.dumps({"signals": [{"code": s} for s in signals]})
    )
    return tx

@pytest.mark.asyncio
async def test_temporal_risk_evolution_unit():
    """Verifies that temporal risk evolution tracks multi-transaction escalation trajectories."""
    txs = [
        create_mock_tx("TX-1", 2500.0, 60, 15.0, "LOW", "Coimbatore", ["NORMAL_TX"]),
        create_mock_tx("TX-2", 35000.0, 40, 48.0, "MEDIUM", "Coimbatore", ["NEW_DEVICE_DETECTED"]),
        create_mock_tx("TX-3", 85000.0, 20, 78.0, "HIGH", "Mumbai", ["LOCATION_ANOMALY", "NEW_DEVICE_DETECTED"]),
        create_mock_tx("TX-4", 120000.0, 5, 94.0, "CRITICAL", "New Delhi", ["IMPOSSIBLE_TRAVEL_VELOCITY", "EXTREME_AMOUNT_OUTLIER"]),
    ]

    trajectory = risk_evolution_engine.analyze_trajectory("ACC-IN-TEST", txs)

    assert trajectory.account_id == "ACC-IN-TEST"
    assert trajectory.trajectory_levels[-1] == "CRITICAL"
    assert trajectory.trajectory_levels[0] == "LOW"
    assert trajectory.is_escalating is True
    assert trajectory.risk_growth_rate > 0
    assert trajectory.escalation_points_count >= 2
    assert "IMPOSSIBLE_TRAVEL_VELOCITY" in trajectory.accumulated_signals
    assert len(trajectory.timeline_points) == 4

@pytest.mark.asyncio
async def test_signal_confluence_unit():
    """Verifies that multi-weak-signal co-occurrence produces non-linear compounding."""
    # Isolated signal: no confluence boost
    single_res = signal_confluence_engine.evaluate(["NORMAL_TX"])
    assert single_res.has_confluence is False
    assert single_res.compounding_multiplier == 1.0

    # Multi-vector confluence: ATO
    ato_res = signal_confluence_engine.evaluate([
        "NEW_DEVICE_DETECTED",
        "IMPOSSIBLE_TRAVEL_VELOCITY",
        "EXTREME_AMOUNT_OUTLIER"
    ])
    assert ato_res.has_confluence is True
    assert ato_res.compounding_multiplier > 1.0
    assert ato_res.combined_risk_boost > 0
    assert "ACCOUNT_TAKEOVER_CONFLUENCE" in ato_res.confluence_name

@pytest.mark.asyncio
async def test_change_point_detection_unit():
    """Verifies statistical change-point detection between historical baseline and current activity."""
    account = Account(
        id="ACC-IN-TEST",
        holder_name="Ramesh Sundaram",
        primary_bank="HDFC Bank",
        typical_city="Coimbatore",
        avg_amount=2500.0,
        risk_rating="LOW"
    )

    txs = [
        create_mock_tx("TX-1", 2500.0, 120, 15.0, "LOW", "Coimbatore", ["NORMAL_TX"]),
        create_mock_tx("TX-2", 35000.0, 60, 55.0, "MEDIUM", "Coimbatore", ["NEW_DEVICE_DETECTED"]),
        create_mock_tx("TX-3", 85000.0, 30, 82.0, "HIGH", "Mumbai", ["LOCATION_ANOMALY"]),
        create_mock_tx("TX-4", 120000.0, 5, 95.0, "CRITICAL", "New Delhi", ["IMPOSSIBLE_TRAVEL_VELOCITY"]),
    ]

    cp = change_point_engine.detect_change_point(account, txs)

    assert cp.regime_shift_detected is True
    assert cp.deviation_magnitude >= 10.0
    assert "TRANSACTION_VALUE" in cp.affected_dimensions
    assert "LOCATION_DISPERSION" in cp.affected_dimensions
    assert cp.change_point_tx_id is not None
    assert "Statistical regime transition" in cp.narrative

@pytest.mark.asyncio
async def test_fraud_pattern_and_story_generation():
    """Verifies synthesis of human-readable pattern hypotheses and 7-stage causal narrative."""
    account = Account(
        id="ACC-IN-TEST",
        holder_name="Ramesh Sundaram",
        primary_bank="HDFC Bank",
        typical_city="Coimbatore",
        avg_amount=2500.0,
        risk_rating="LOW"
    )
    txs = [
        create_mock_tx("TX-1", 2500.0, 60, 15.0, "LOW", "Coimbatore", ["NORMAL_TX"]),
        create_mock_tx("TX-2", 35000.0, 40, 48.0, "MEDIUM", "Coimbatore", ["NEW_DEVICE_DETECTED"]),
        create_mock_tx("TX-3", 85000.0, 20, 78.0, "HIGH", "Mumbai", ["LOCATION_ANOMALY", "NEW_DEVICE_DETECTED"]),
        create_mock_tx("TX-4", 120000.0, 5, 94.0, "CRITICAL", "New Delhi", ["IMPOSSIBLE_TRAVEL_VELOCITY", "EXTREME_AMOUNT_OUTLIER"]),
    ]

    evolution = risk_evolution_engine.analyze_trajectory("ACC-IN-TEST", txs)
    confluence = signal_confluence_engine.evaluate(evolution.accumulated_signals)
    change_point = change_point_engine.detect_change_point(account, txs)
    
    # Mock network propagation
    from app.schemas.investigation import CrossAccountPropagation, NetworkLink
    network = CrossAccountPropagation(
        account_id="ACC-IN-TEST",
        network_exposure_score=85.0,
        cluster_classification="POTENTIAL_COORDINATED_ACTIVITY",
        correlated_accounts_count=2,
        shared_devices=["DEV-IN-SHARED-99"],
        network_links=[
            NetworkLink(
                connected_account_id="ACC-IN-1002",
                relationship_type="Shared Hardware Fingerprint",
                shared_entity="DEV-IN-SHARED-99",
                link_grade="POTENTIAL_COORDINATED_ACTIVITY",
                explanation="Shared hardware linked to high risk entity"
            )
        ]
    )

    patterns = pattern_engine.synthesize_patterns(evolution, confluence, change_point, network)
    assert len(patterns) > 0
    top_pattern = patterns[0]
    assert "Account Takeover" in top_pattern.pattern_name or "Coordinated" in top_pattern.pattern_name
    assert top_pattern.confidence_score >= 0.85

    story = fraud_story_engine.generate_story(
        account=account,
        evolution=evolution,
        confluence=confluence,
        change_point=change_point,
        network=network,
        patterns=patterns,
        latest_tx=txs[-1]
    )

    assert story.timeline != ""
    assert story.behaviour_change != ""
    assert story.signal_confluence != ""
    assert story.network_relationship != ""
    assert story.risk_escalation != ""
    assert story.current_assessment != ""
    assert story.recommended_action != ""
    assert "Ramesh Sundaram" in story.full_narrative

@pytest.mark.asyncio
async def test_investigation_priority_scoring():
    """Verifies dynamic calculation of investigative triage priority score."""
    from app.schemas.investigation import CrossAccountPropagation, SignalConfluence, ChangePointAnalysis
    
    confluence = SignalConfluence(
        has_confluence=True,
        confluence_name="ACCOUNT_TAKEOVER_CONFLUENCE",
        compounding_multiplier=1.65,
        combined_risk_boost=35.0,
        contributing_signals=["NEW_DEVICE_DETECTED", "IMPOSSIBLE_TRAVEL_VELOCITY"],
        confidence_score=0.94,
        description="Test"
    )
    change_point = ChangePointAnalysis(
        regime_shift_detected=True,
        historical_avg_amount=2500.0,
        historical_typical_city="Coimbatore",
        recent_avg_amount=85000.0,
        deviation_magnitude=34.0,
        affected_dimensions=["TRANSACTION_VALUE", "LOCATION_DISPERSION"],
        narrative="Test"
    )
    network = CrossAccountPropagation(
        account_id="ACC-TEST",
        network_exposure_score=85.0,
        cluster_classification="POTENTIAL_COORDINATED_ACTIVITY",
        correlated_accounts_count=2,
        shared_devices=["DEV-TEST"],
        network_links=[]
    )

    tier, score = investigation_priority_engine.calculate_priority(
        current_risk_score=92.0,
        is_escalating=True,
        risk_growth_rate=25.0,
        confluence=confluence,
        change_point=change_point,
        network=network,
        signals_count=4
    )

    assert tier == "URGENT"
    assert score >= 75.0

@pytest.mark.asyncio
async def test_innovation_api_endpoints_and_judge_demo():
    """Verifies all REST API endpoints for investigations and executes the live Judge Demo scenario."""
    async with app.router.lifespan_context(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            # 1. List investigations
            res_list = await client.get("/api/investigations")
            assert res_list.status_code == 200
            investigations = res_list.json()
            assert isinstance(investigations, list)
            assert len(investigations) > 0

            first_inv = investigations[0]
            assert "account_id" in first_inv
            assert "investigation_priority" in first_inv
            assert "priority_score" in first_inv
            assert "current_risk_level" in first_inv

            sample_acc_id = first_inv["account_id"]

            # 2. Get full dossier for sample account
            res_dossier = await client.get(f"/api/investigations/{sample_acc_id}")
            assert res_dossier.status_code == 200
            dossier = res_dossier.json()
            assert dossier["summary"]["account_id"] == sample_acc_id
            assert "evolution" in dossier
            assert "confluence" in dossier
            assert "change_point" in dossier
            assert "network_propagation" in dossier
            assert "patterns" in dossier
            assert "fraud_story" in dossier

            # 3. Specific sub-endpoints
            res_evol = await client.get(f"/api/investigations/{sample_acc_id}/evolution")
            assert res_evol.status_code == 200
            evol = res_evol.json()
            assert "trajectory_levels" in evol
            assert "risk_growth_rate" in evol

            res_timeline = await client.get(f"/api/investigations/{sample_acc_id}/timeline")
            assert res_timeline.status_code == 200
            assert isinstance(res_timeline.json(), list)

            res_patterns = await client.get(f"/api/investigations/{sample_acc_id}/patterns")
            assert res_patterns.status_code == 200
            assert isinstance(res_patterns.json(), list)

            # 4. Trigger Live Judge Demo Scenario (ACC-IN-1043)
            res_demo = await client.post("/api/investigations/judge-demo")
            assert res_demo.status_code == 200
            demo_dossier = res_demo.json()

            assert demo_dossier["summary"]["account_id"] == "ACC-IN-1043"
            assert demo_dossier["summary"]["investigation_priority"] in ["INVESTIGATE", "URGENT"]
            assert demo_dossier["summary"]["current_risk_level"] in ["HIGH", "CRITICAL"]
            assert len(demo_dossier["evolution"]["timeline_points"]) >= 4
            assert len(demo_dossier["patterns"]) > 0
            assert demo_dossier["fraud_story"]["recommended_action"] != ""

            # 5. Verify Demo Reset Mechanism (Repeatable Multi-Cycle)
            res_reset = await client.post("/api/investigations/judge-demo/reset")
            assert res_reset.status_code == 200
            reset_dossier = res_reset.json()
            assert reset_dossier["summary"]["account_id"] == "ACC-IN-1043"
            assert reset_dossier["summary"]["current_risk_level"] == "LOW"
            assert reset_dossier["evolution"]["is_escalating"] is False
            assert len(reset_dossier["evolution"]["timeline_points"]) == 1
            assert reset_dossier["evolution"]["timeline_points"][0]["amount"] == 2500.0

            # 6. Re-run Judge Demo after reset (Cycle 2)
            res_demo_2 = await client.post("/api/investigations/judge-demo")
            assert res_demo_2.status_code == 200
            demo_2 = res_demo_2.json()
            assert demo_2["summary"]["current_risk_level"] in ["HIGH", "CRITICAL"]
            assert len(demo_2["evolution"]["timeline_points"]) >= 4

            # 7. Reset again (Cycle 2 Clean)
            res_reset_2 = await client.post("/api/investigations/judge-demo/reset")
            assert res_reset_2.status_code == 200
            assert res_reset_2.json()["summary"]["current_risk_level"] == "LOW"

