import pytest
from datetime import datetime, timedelta
from app.utils.geo import haversine_distance, calculate_speed_kmh
from app.services.behavioral import behavioral_engine
from app.services.location import location_engine
from app.services.velocity import velocity_engine
from app.services.graph_service import GraphIntelligenceService
from app.services.risk_fusion import risk_fusion
from app.models.account import Account
from app.models.transaction import Transaction
from app.schemas.risk import SignalEvidence

def test_haversine_distance():
    # Coimbatore to Mumbai is ~990 km
    d = haversine_distance(11.0168, 76.9558, 19.0760, 72.8777)
    assert 950 < d < 1050

def test_calculate_speed_impossible_travel():
    # 990 km in 15 minutes (900s) -> speed is 3,960 km/h
    speed = calculate_speed_kmh(990.0, 900.0)
    assert speed > 3500.0

def test_behavioral_z_score_outlier():
    acc = Account(
        id="ACC-IN-TEST-1",
        holder_name="Arun Kumar",
        email="arun.kumar@gmail.com",
        avg_amount=3500.0,
        std_amount=950.0
    )
    # ₹1,25,000 is >35x avg and extreme Z-score!
    signals = behavioral_engine.evaluate(
        account=acc,
        amount=125000.0,
        merchant_category="ELECTRONICS",
        timestamp=datetime(2026, 9, 18, 14, 0, 0),
        recent_categories=["GROCERY"]
    )
    codes = [s.code for s in signals]
    assert "EXTREME_AMOUNT_OUTLIER" in codes

def test_velocity_burst():
    now = datetime.utcnow()
    # Create 4 transactions in the last 30 seconds
    recent = [
        Transaction(id=f"TXN-IN-T{i}", timestamp=now - timedelta(seconds=i*5), amount=250.0, account_id="ACC-IN-1001", device_id="DEV-IN-1001-PRIM")
        for i in range(4)
    ]
    signals, c1m, c5m = velocity_engine.evaluate(
        current_time=now,
        current_amount=2450.0,
        recent_transactions=recent
    )
    codes = [s.code for s in signals]
    assert "RAPID_BURST_VELOCITY" in codes
    assert c1m >= 4

def test_graph_circular_layering():
    gs = GraphIntelligenceService()
    # A -> B -> C
    gs.add_account("ACC-IN-MULE-A", "Mule Node A")
    gs.add_account("ACC-IN-MULE-B", "Mule Node B")
    gs.add_account("ACC-IN-MULE-C", "Mule Node C")
    gs.record_transaction("ACC-IN-MULE-A", "ACC-IN-MULE-B", "IMPS Transfer", 25000.0, datetime.utcnow().isoformat(), "DEV-IN-SHARED-MULE", "LOW")
    gs.record_transaction("ACC-IN-MULE-B", "ACC-IN-MULE-C", "IMPS Transfer", 25000.0, datetime.utcnow().isoformat(), "DEV-IN-SHARED-MULE", "LOW")

    # Now transaction C -> A closes the cycle!
    signals, is_circular, share_count = gs.evaluate("ACC-IN-MULE-C", "ACC-IN-MULE-A", "DEV-IN-SHARED-MULE")
    assert is_circular is True
    codes = [s.code for s in signals]
    assert "CIRCULAR_TRANSFER_RING" in codes

def test_risk_fusion_impossible_travel_override():
    sig = SignalEvidence(
        code="IMPOSSIBLE_TRAVEL_VELOCITY",
        name="Impossible Travel Velocity",
        category="LOCATION",
        points=45.0,
        observed_value="3960 km/h",
        baseline_value="800 km/h",
        severity="CRITICAL",
        description="Speed required between Coimbatore and Mumbai exceeds commercial aircraft capabilities"
    )
    assessment = risk_fusion.fuse(
        transaction_id="TXN-IN-TEST",
        signals=[sig],
        ml_score=60.0,
        speed_kmh=3960.0,
        dist_km=990.0
    )
    # Impossible travel hard gate enforces at least 80 risk score -> HIGH or CRITICAL
    assert assessment.risk_score >= 80.0
    assert assessment.risk_level in ["HIGH", "CRITICAL"]
    assert assessment.action_taken in ["HOLD", "BLOCK"]
