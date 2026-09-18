import httpx
import json
import time
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_URL = "http://127.0.0.1:8000"

def run_verification():
    print("=" * 60)
    print("STARTING LIVE RUNTIME VERIFICATION OF FRAUD-X ENGINE")
    print("=" * 60)
    
    with httpx.Client(base_url=BASE_URL, timeout=15.0) as client:
        # 1. Health & Root
        res_root = client.get("/")
        print(f"\n[1] GET / -> Status {res_root.status_code}")
        print("    Payload:", res_root.json())
        assert res_root.status_code == 200

        res_health = client.get("/api/health")
        print(f"\n[2] GET /api/health -> Status {res_health.status_code}")
        print("    Payload:", json.dumps(res_health.json(), indent=2))
        assert res_health.status_code == 200

        # 2. Accounts
        res_accounts = client.get("/api/accounts?limit=50")
        print(f"\n[3] GET /api/accounts -> Status {res_accounts.status_code}")
        accounts = res_accounts.json()
        print(f"    Total accounts loaded: {len(accounts)}")
        assert len(accounts) >= 30

        # 3. Analytics
        res_overview = client.get("/api/analytics/overview")
        print(f"\n[4] GET /api/analytics/overview -> Status {res_overview.status_code}")
        print("    Payload:", json.dumps(res_overview.json(), indent=2))

        res_dist = client.get("/api/analytics/risk-distribution")
        print(f"\n[5] GET /api/analytics/risk-distribution -> Status {res_dist.status_code}")
        print("    Distribution categories:", res_dist.json()["distribution"])

        # 4. Graph Network
        res_graph = client.get("/api/graph/network")
        print(f"\n[6] GET /api/graph/network -> Status {res_graph.status_code}")
        graph_data = res_graph.json()
        print(f"    Graph Nodes: {len(graph_data['nodes'])}, Edges: {len(graph_data['edges'])}")

        # 5. CONTROLLED SCENARIOS VERIFICATION
        print("\n" + "=" * 60)
        print("RUNNING CONTROLLED SCENARIOS TEST SUITE (Points 5, 6, 7, 8)")
        print("=" * 60)

        # Scenario A: Normal Transaction on ACC-IN-1010 (Clean Account at Home Location)
        acc_a_id = "ACC-IN-1010"
        res_acc_a = client.get(f"/api/accounts/{acc_a_id}").json()
        acc_a = res_acc_a["account"]
        dev_a = res_acc_a["devices"][0]["id"] if res_acc_a["devices"] else "DEV-IN-1010-PRIM"

        normal_tx = {
            "account_id": acc_a_id,
            "amount": round(acc_a["avg_amount"] * 0.9, 2),
            "merchant_name": "DMart Supermarket",
            "merchant_category": "GROCERY",
            "device_id": dev_a,
            "location_city": acc_a["typical_city"],
            "location_country": acc_a["typical_country"],
            "location_lat": acc_a["typical_location_lat"],
            "location_lon": acc_a["typical_location_lon"],
            "transaction_type": "UPI"
        }
        res_a = client.post("/api/transactions/ingest", json=normal_tx)
        tx_a = res_a.json()
        print(f"\n[Scenario A: NORMAL ({acc_a_id})]")
        print(f"   Score: {tx_a['risk_score']} / 100.0 | Level: {tx_a['risk_level']} | Action: {tx_a['action_taken']}")
        print(f"   Signals: {[s['code'] for s in tx_a['assessment']['signals']]}")
        assert tx_a["risk_score"] < 30.0
        assert tx_a["risk_level"] == "LOW"
        assert tx_a["action_taken"] == "ALLOW"

        # Scenario B: High-Value Transaction on ACC-IN-1011 (Amount 18x Baseline)
        acc_b_id = "ACC-IN-1011"
        res_acc_b = client.get(f"/api/accounts/{acc_b_id}").json()
        acc_b = res_acc_b["account"]
        dev_b = res_acc_b["devices"][0]["id"] if res_acc_b["devices"] else "DEV-IN-1011-PRIM"

        high_val_tx = {
            "account_id": acc_b_id,
            "amount": round(acc_b["avg_amount"] * 18.0, 2),
            "merchant_name": "Tanishq Jewellers",
            "merchant_category": "RETAIL",
            "device_id": dev_b,
            "location_city": acc_b["typical_city"],
            "location_country": acc_b["typical_country"],
            "location_lat": acc_b["typical_location_lat"],
            "location_lon": acc_b["typical_location_lon"],
            "transaction_type": "NET_BANKING"
        }
        res_b = client.post("/api/transactions/ingest", json=high_val_tx)
        tx_b = res_b.json()
        print(f"\n[Scenario B: HIGH-VALUE ({acc_b_id})]")
        print(f"   Score: {tx_b['risk_score']} / 100.0 | Level: {tx_b['risk_level']} | Action: {tx_b['action_taken']}")
        print(f"   Signals: {[s['code'] for s in tx_b['assessment']['signals']]}")
        assert tx_b["risk_score"] > tx_a["risk_score"]
        assert any(s["code"] in ["EXTREME_AMOUNT_OUTLIER", "AMOUNT_ABOVE_BASELINE"] for s in tx_b['assessment']['signals'])

        # Scenario C: New Unrecognized Device on ACC-IN-1012
        acc_c_id = "ACC-IN-1012"
        res_acc_c = client.get(f"/api/accounts/{acc_c_id}").json()
        acc_c = res_acc_c["account"]

        import uuid
        new_dev_id = f"DEV-IN-NEW-HARDWARE-{uuid.uuid4().hex[:6].upper()}"
        new_dev_tx = {
            "account_id": acc_c_id,
            "amount": round(acc_c["avg_amount"], 2),
            "merchant_name": "Flipkart Online",
            "merchant_category": "E_COMMERCE",
            "device_id": new_dev_id,
            "location_city": acc_c["typical_city"],
            "location_country": acc_c["typical_country"],
            "location_lat": acc_c["typical_location_lat"],
            "location_lon": acc_c["typical_location_lon"],
            "transaction_type": "UPI"
        }
        res_c = client.post("/api/transactions/ingest", json=new_dev_tx)
        tx_c = res_c.json()
        print(f"\n[Scenario C: NEW DEVICE ({acc_c_id})]")
        print(f"   Score: {tx_c['risk_score']} / 100.0 | Level: {tx_c['risk_level']} | Action: {tx_c['action_taken']}")
        print(f"   Signals: {[s['code'] for s in tx_c['assessment']['signals']]}")
        assert any(s["code"] == "NEW_DEVICE_DETECTED" for s in tx_c['assessment']['signals'])

        # Scenario D: Unusual Location & Impossible Travel on ACC-IN-1013 (Coimbatore -> Mumbai)
        acc_d_id = "ACC-IN-1013"
        res_acc_d = client.get(f"/api/accounts/{acc_d_id}").json()
        acc_d = res_acc_d["account"]
        dev_d = res_acc_d["devices"][0]["id"] if res_acc_d["devices"] else "DEV-IN-1013-PRIM"

        # Step 1: Base tx in Coimbatore
        tx_d1_data = {
            "account_id": acc_d_id,
            "amount": 850.0,
            "merchant_name": "A2B Sweets Coimbatore",
            "merchant_category": "FOOD_DELIVERY",
            "device_id": dev_d,
            "location_city": "Coimbatore",
            "location_country": "India",
            "location_lat": 11.0168,
            "location_lon": 76.9558,
            "transaction_type": "UPI"
        }
        res_d1 = client.post("/api/transactions/ingest", json=tx_d1_data)
        assert res_d1.status_code == 200
        time.sleep(0.2)

        # Step 2: Instant tx 990 km away in Mumbai (Speed > 10,000 km/h)
        geo_tx = {
            "account_id": acc_d_id,
            "amount": 125000.0,
            "merchant_name": "Croma Electronics Mumbai",
            "merchant_category": "ELECTRONICS",
            "device_id": "DEV-IN-TRAVEL-MUMBAI-REMOTE",
            "location_city": "Mumbai",
            "location_country": "India",
            "location_lat": 19.0760,
            "location_lon": 72.8777,
            "transaction_type": "CREDIT_CARD"
        }
        res_d = client.post("/api/transactions/ingest", json=geo_tx)
        tx_d = res_d.json()
        print(f"\n[Scenario D: IMPOSSIBLE TRAVEL VELOCITY ({acc_d_id})]")
        print(f"   Score: {tx_d['risk_score']} / 100.0 | Level: {tx_d['risk_level']} | Action: {tx_d['action_taken']}")
        print(f"   Signals: {[s['code'] for s in tx_d['assessment']['signals']]}")
        if tx_d['assessment']['speed_kmh']:
            print(f"   Speed: {tx_d['assessment']['speed_kmh']:,.0f} km/h (Distance: {tx_d['assessment']['distance_km']:,.0f} km)")
        assert tx_d["risk_score"] >= 75.0
        assert tx_d["action_taken"] in ["HOLD", "BLOCK"]
        assert any(s["code"] == "IMPOSSIBLE_TRAVEL_VELOCITY" for s in tx_d['assessment']['signals'])

        # Scenario E: Rapid Transaction Burst on ACC-IN-1014
        acc_e_id = "ACC-IN-1014"
        res_acc_e = client.get(f"/api/accounts/{acc_e_id}").json()
        acc_e = res_acc_e["account"]
        burst_dev = "DEV-IN-RAPID-SCRIPT-BOT"
        burst_scores = []
        for i in range(5):
            b_tx = {
                "account_id": acc_e_id,
                "amount": 250.00 + (i * 50),
                "merchant_name": f"FastPay UPI Auth {i}",
                "merchant_category": "QR_PAYMENT",
                "device_id": burst_dev,
                "location_city": acc_e["typical_city"],
                "location_country": acc_e["typical_country"],
                "location_lat": acc_e["typical_location_lat"],
                "location_lon": acc_e["typical_location_lon"],
                "transaction_type": "UPI"
            }
            res_e = client.post("/api/transactions/ingest", json=b_tx)
            burst_scores.append(res_e.json()["risk_score"])
            time.sleep(0.05)
        print(f"\n[Scenario E: VELOCITY BURST ({acc_e_id})]")
        print(f"   Scores progression across 5 sub-second txs: {burst_scores}")
        assert burst_scores[-1] > burst_scores[0]
        assert burst_scores[-1] >= 35.0

        # Scenario F: Combined Multi-Suspicious Attack Confluence on ACC-IN-1015
        acc_f_id = "ACC-IN-1015"
        res_acc_f = client.get(f"/api/accounts/{acc_f_id}").json()
        acc_f = res_acc_f["account"]

        confluence_tx = {
            "account_id": acc_f_id,
            "amount": 480000.0,
            "merchant_name": "Reliance Digital Flagship",
            "merchant_category": "ELECTRONICS",
            "device_id": "DEV-IN-COMPROMISED-MULE-SYNDICATE-01",
            "location_city": "New Delhi",
            "location_country": "India",
            "location_lat": 28.6139,
            "location_lon": 77.2090,
            "transaction_type": "IMPS"
        }
        res_f = client.post("/api/transactions/ingest", json=confluence_tx)
        tx_f = res_f.json()
        print(f"\n[Scenario F: COMBINED MULTI-SUSPICIOUS CONFLUENCE ({acc_f_id})]")
        print(f"   Score: {tx_f['risk_score']} / 100.0 | Level: {tx_f['risk_level']} | Action: {tx_f['action_taken']}")
        print("   Triggered Evidence Signals:")
        for s in tx_f['assessment']['signals']:
            print(f"     • [{s['category']}] {s['name']}: {s['observed_value']} (+{s['points']} pts)")
        print("   Primary Causal Explanations:")
        for r in tx_f['assessment']['primary_reasons']:
            print(f"     - {r}")

        assert tx_f["risk_score"] >= 85.0
        assert tx_f["risk_level"] == "CRITICAL"
        assert tx_f["action_taken"] == "BLOCK"
        assert len(tx_f['assessment']['signals']) >= 3
        # Confluence risk is dramatically higher than normal
        assert tx_f["risk_score"] - tx_a["risk_score"] > 60.0

        # 6. AI Analyst On-Demand Investigation
        print("\n" + "=" * 60)
        print("AI ANALYST VERIFICATION (Point 5 & 7)")
        print("=" * 60)
        res_ai = client.post(f"/api/ai/investigate/{tx_f['id']}")
        assert res_ai.status_code == 200
        ai_narrative = res_ai.json()
        print(f"\n[AI Analyst Report for Tx {tx_f['id']}]")
        print(f"Executive Summary:\n  {ai_narrative['executive_summary']}")
        print(f"\nForensic Narrative:\n  {ai_narrative['forensic_narrative'][:250]}...")
        print(f"\nCorrelation Analysis:\n  {ai_narrative['correlation_analysis']}")
        print(f"\nRecommended Action:\n  {ai_narrative['recommended_action']} (Confidence: {ai_narrative['confidence_score'] * 100:.0f}%)")
        print(f"Immediate Mitigations:")
        for m in ai_narrative['immediate_mitigations']:
            print(f"  • {m}")

        # 7. Simulator Trigger Verification
        print("\n" + "=" * 60)
        print("ATTACK SIMULATOR ENDPOINTS VERIFICATION")
        print("=" * 60)
        res_sim = client.post("/api/simulator/scenario", json={"scenario": "ATO"})
        assert res_sim.status_code == 200
        sim_res = res_sim.json()
        print(f"Triggered ATO Scenario -> Success: {sim_res['success']}, Injected: {sim_res['injected_count']} transactions")

        print("\n" + "=" * 60)
        print("ALL LIVE RUNTIME VERIFICATION CHECKS PASSED PERFECTLY!")
        print("=" * 60)

if __name__ == "__main__":
    run_verification()
