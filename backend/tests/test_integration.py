import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from datetime import datetime, timedelta
from app.main import app

@pytest.mark.asyncio
async def test_full_application_lifecycle_and_endpoints():
    async with app.router.lifespan_context(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            # 1. Health & Root
            res_root = await client.get("/")
            assert res_root.status_code == 200
            assert res_root.json()["status"] == "OPERATIONAL"

            res_health = await client.get("/api/health")
            assert res_health.status_code == 200
            health_data = res_health.json()
            assert health_data["status"] == "HEALTHY"
            assert health_data["models"]["behavioral_engine"] == "ACTIVE"
            assert health_data["models"]["graph_engine"] == "ACTIVE"

            # 2. Accounts Endpoint & Seed Data Verification
            res_accounts = await client.get("/api/accounts?limit=30")
            assert res_accounts.status_code == 200
            accounts = res_accounts.json()
            assert len(accounts) > 0
            # Pick a clean account with LOW risk rating
            target_account = next((a for a in accounts if a.get("risk_rating") == "LOW"), accounts[-1])
            acc_id = target_account["id"]
            assert "avg_amount" in target_account
            assert target_account["avg_amount"] > 0

            # Detailed Account Profile
            res_profile = await client.get(f"/api/accounts/{acc_id}")
            assert res_profile.status_code == 200
            profile = res_profile.json()
            assert "account" in profile
            assert "devices" in profile

            # 3. Analytics Endpoints
            res_overview = await client.get("/api/analytics/overview")
            assert res_overview.status_code == 200
            ov = res_overview.json()
            assert ov["total_transactions"] >= 0
            assert "processing_engine_status" in ov

            res_dist = await client.get("/api/analytics/risk-distribution")
            assert res_dist.status_code == 200
            dist = res_dist.json()
            assert "distribution" in dist
            assert len(dist["distribution"]) == 4

            # 4. Graph Network Endpoint
            res_graph = await client.get("/api/graph/network")
            assert res_graph.status_code == 200
            graph_data = res_graph.json()
            assert "nodes" in graph_data
            assert "edges" in graph_data

            # 5. Pipeline Test 1: Normal Legitimate Transaction (on isolated account)
            import uuid
            acc_a = accounts[5] if len(accounts) > 5 else accounts[0]
            res_pa = await client.get(f"/api/accounts/{acc_a['id']}")
            prof_a = res_pa.json()
            home_lat_a = prof_a["account"]["typical_location_lat"]
            home_lon_a = prof_a["account"]["typical_location_lon"]
            home_city_a = prof_a["account"]["typical_city"]
            home_country_a = prof_a["account"]["typical_country"]
            dev_a = prof_a["devices"][0]["id"] if prof_a["devices"] else "DEV-IN-LEGIT-1"

            norm_payload = {
                "account_id": acc_a["id"],
                "amount": round(acc_a["avg_amount"] * 0.9, 2),
                "currency": "INR",
                "merchant_name": "DMart Hypermarket",
                "merchant_category": "GROCERY",
                "device_id": dev_a,
                "location_city": home_city_a,
                "location_country": home_country_a,
                "location_lat": home_lat_a,
                "location_lon": home_lon_a,
                "transaction_type": "UPI"
            }
            res_norm = await client.post("/api/transactions/ingest", json=norm_payload)
            assert res_norm.status_code == 200
            norm_tx = res_norm.json()
            assert norm_tx["risk_score"] < 30.0
            assert norm_tx["risk_level"] == "LOW"
            assert norm_tx["action_taken"] == "ALLOW"

            # 6. Pipeline Test 2: High-Value Anomaly (₹1,25,000 Outlier on acc_b)
            acc_b = accounts[6] if len(accounts) > 6 else accounts[0]
            res_pb = await client.get(f"/api/accounts/{acc_b['id']}")
            prof_b = res_pb.json()
            dev_b = prof_b["devices"][0]["id"] if prof_b["devices"] else "DEV-IN-LEGIT-2"

            high_val_payload = {
                "account_id": acc_b["id"],
                "amount": 125000.0,
                "currency": "INR",
                "merchant_name": "Tanishq Jewellers",
                "merchant_category": "RETAIL",
                "device_id": dev_b,
                "location_city": prof_b["account"]["typical_city"],
                "location_country": prof_b["account"]["typical_country"],
                "location_lat": prof_b["account"]["typical_location_lat"],
                "location_lon": prof_b["account"]["typical_location_lon"],
                "transaction_type": "NET_BANKING"
            }
            res_high_val = await client.post("/api/transactions/ingest", json=high_val_payload)
            assert res_high_val.status_code == 200
            high_val_tx = res_high_val.json()
            assert high_val_tx["risk_score"] > norm_tx["risk_score"]
            assert any(s["code"] in ["EXTREME_AMOUNT_OUTLIER", "AMOUNT_ABOVE_BASELINE"] for s in high_val_tx["assessment"]["signals"])

            # 7. Pipeline Test 3: New Device on acc_c
            acc_c = accounts[7] if len(accounts) > 7 else accounts[0]
            res_pc = await client.get(f"/api/accounts/{acc_c['id']}")
            prof_c = res_pc.json()
            unique_new_dev_id = f"DEV-IN-NEW-{uuid.uuid4().hex[:8].upper()}"

            new_dev_payload = {
                "account_id": acc_c["id"],
                "amount": round(acc_c["avg_amount"], 2),
                "currency": "INR",
                "merchant_name": "Flipkart Online",
                "merchant_category": "E_COMMERCE",
                "device_id": unique_new_dev_id,
                "location_city": prof_c["account"]["typical_city"],
                "location_country": prof_c["account"]["typical_country"],
                "location_lat": prof_c["account"]["typical_location_lat"],
                "location_lon": prof_c["account"]["typical_location_lon"],
                "transaction_type": "UPI"
            }
            res_new_dev = await client.post("/api/transactions/ingest", json=new_dev_payload)
            assert res_new_dev.status_code == 200
            new_dev_tx = res_new_dev.json()
            assert any(s["code"] == "NEW_DEVICE_DETECTED" for s in new_dev_tx["assessment"]["signals"])

            # 8. Pipeline Test 4: Impossible Travel on acc_d
            acc_d = accounts[8] if len(accounts) > 8 else accounts[0]
            res_pd = await client.get(f"/api/accounts/{acc_d['id']}")
            prof_d = res_pd.json()
            h_city_d = prof_d["account"]["typical_city"]
            dev_d = prof_d["devices"][0]["id"] if prof_d["devices"] else "DEV-IN-LEGIT-4"

            # Base transaction at home
            await client.post("/api/transactions/ingest", json={
                "account_id": acc_d["id"],
                "amount": 500.0,
                "currency": "INR",
                "merchant_name": "Local Grocery",
                "merchant_category": "GROCERY",
                "device_id": dev_d,
                "location_city": h_city_d,
                "location_country": "India",
                "location_lat": prof_d["account"]["typical_location_lat"],
                "location_lon": prof_d["account"]["typical_location_lon"],
                "transaction_type": "UPI"
            })

            dest_city = "New Delhi" if h_city_d == "Mumbai" else "Mumbai"
            dest_lat = 28.6139 if dest_city == "New Delhi" else 19.0760
            dest_lon = 77.2090 if dest_city == "New Delhi" else 72.8777

            travel_payload = {
                "account_id": acc_d["id"],
                "amount": 25000.0,
                "currency": "INR",
                "merchant_name": "Croma Electronics Remote",
                "merchant_category": "ELECTRONICS",
                "device_id": f"DEV-IN-TRAVEL-{uuid.uuid4().hex[:6].upper()}",
                "location_city": dest_city,
                "location_country": "India",
                "location_lat": dest_lat,
                "location_lon": dest_lon,
                "transaction_type": "CREDIT_CARD"
            }
            res_travel = await client.post("/api/transactions/ingest", json=travel_payload)
            assert res_travel.status_code == 200
            travel_tx = res_travel.json()
            assert travel_tx["risk_score"] >= 75.0
            assert travel_tx["action_taken"] in ["HOLD", "BLOCK"]
            assert any(s["code"] == "IMPOSSIBLE_TRAVEL_VELOCITY" for s in travel_tx["assessment"]["signals"])

            # 9. Pipeline Test 5: Multi-Suspicious Attack Confluence on acc_e
            acc_e = accounts[9] if len(accounts) > 9 else accounts[0]
            attack_dev_id = f"DEV-IN-SYNDICATE-ATTACK-{uuid.uuid4().hex[:6].upper()}"
            confluence_payload = {
                "account_id": acc_e["id"],
                "amount": 480000.0,
                "currency": "INR",
                "merchant_name": "CoinDCX Crypto Portal",
                "merchant_category": "CRYPTO_EXCHANGE",
                "device_id": attack_dev_id,
                "location_city": "New Delhi",
                "location_country": "India",
                "location_lat": 28.6139,
                "location_lon": 77.2090,
                "transaction_type": "IMPS"
            }
            res_confluence = await client.post("/api/transactions/ingest", json=confluence_payload)
            assert res_confluence.status_code == 200
            confluence_tx = res_confluence.json()
            assert confluence_tx["risk_score"] >= 85.0
            assert confluence_tx["risk_level"] == "CRITICAL"
            assert confluence_tx["action_taken"] == "BLOCK"
            
            # Verify Explainability
            assessment = confluence_tx["assessment"]
            assert len(assessment["primary_reasons"]) >= 2
            assert len(assessment["signals"]) >= 3
            for sig in assessment["signals"]:
                assert "points" in sig
                assert "observed_value" in sig
                assert "baseline_value" in sig
                assert "description" in sig

            # 10. AI Analyst Investigation Endpoint
            res_ai = await client.post(f"/api/ai/investigate/{confluence_tx['id']}")
            assert res_ai.status_code == 200
            ai_data = res_ai.json()
            assert "executive_summary" in ai_data
            assert "forensic_narrative" in ai_data
            assert "correlation_analysis" in ai_data
            assert "recommended_action" in ai_data
            assert ai_data["recommended_action"] == "BLOCK"
            assert len(ai_data["immediate_mitigations"]) > 0

            # 11. Simulator Endpoints
            res_sim_status = await client.get("/api/simulator/status")
            assert res_sim_status.status_code == 200

            res_sim_scen = await client.post("/api/simulator/scenario", json={"scenario": "CARD_TESTING"})
            assert res_sim_scen.status_code == 200
            sim_data = res_sim_scen.json()
            assert sim_data["success"] is True
            assert sim_data["injected_count"] >= 5

            # 12. Transaction List Endpoint
            res_tx_list = await client.get("/api/transactions?limit=10&min_risk=50")
            assert res_tx_list.status_code == 200
            tx_list = res_tx_list.json()
            assert tx_list["total"] > 0
