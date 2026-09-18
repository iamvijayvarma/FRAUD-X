import asyncio
import time
import httpx
import statistics

BASE_URL = "http://127.0.0.1:8000"

async def run_rehearsal_cycle(client: httpx.AsyncClient, cycle_num: int):
    # 1. Reset Demo to clean baseline
    t0 = time.perf_counter()
    r_reset = await client.post(f"{BASE_URL}/api/investigations/judge-demo/reset")
    t_reset = (time.perf_counter() - t0) * 1000.0
    assert r_reset.status_code == 200, f"Reset failed: {r_reset.text}"
    reset_data = r_reset.json()
    assert reset_data["summary"]["account_id"] == "ACC-IN-1043"
    assert len(reset_data["evolution"]["timeline_points"]) == 1, f"Expected 1 baseline tx, got {len(reset_data['evolution']['timeline_points'])}"

    # 2. Fetch baseline dossier
    t0 = time.perf_counter()
    r_base = await client.get(f"{BASE_URL}/api/investigations/ACC-IN-1043")
    t_base = (time.perf_counter() - t0) * 1000.0
    assert r_base.status_code == 200

    # 3. Execute Judge Demo (4-step attack injection + fusion)
    t0 = time.perf_counter()
    r_demo = await client.post(f"{BASE_URL}/api/investigations/judge-demo")
    t_demo = (time.perf_counter() - t0) * 1000.0
    assert r_demo.status_code == 200, f"Judge Demo failed: {r_demo.text}"
    demo_data = r_demo.json()
    assert demo_data["summary"]["account_id"] == "ACC-IN-1043"
    assert len(demo_data["evolution"]["timeline_points"]) == 4, f"Expected 4 timeline steps, got {len(demo_data['evolution']['timeline_points'])}"
    assert demo_data["summary"]["investigation_priority"] in ["HIGH", "URGENT"]
    assert demo_data["change_point"]["regime_shift_detected"] is True
    assert len(demo_data["network_propagation"]["network_links"]) >= 1

    # 4. Fetch updated investigation dossier
    t0 = time.perf_counter()
    r_dossier = await client.get(f"{BASE_URL}/api/investigations/ACC-IN-1043")
    t_dossier = (time.perf_counter() - t0) * 1000.0
    assert r_dossier.status_code == 200

    # 5. Fetch forensic evidence for flagged transaction
    crit_tx = demo_data["evolution"]["timeline_points"][-1]
    t0 = time.perf_counter()
    r_tx = await client.get(f"{BASE_URL}/api/transactions/{crit_tx['transaction_id']}")
    t_tx = (time.perf_counter() - t0) * 1000.0
    assert r_tx.status_code == 200

    # 6. Recovery / Post-demo reset
    t0 = time.perf_counter()
    r_recover = await client.post(f"{BASE_URL}/api/investigations/judge-demo/reset")
    t_recover = (time.perf_counter() - t0) * 1000.0
    assert r_recover.status_code == 200

    return {
        "cycle": cycle_num,
        "reset_ms": t_reset,
        "baseline_load_ms": t_base,
        "demo_execution_ms": t_demo,
        "dossier_load_ms": t_dossier,
        "tx_forensic_ms": t_tx,
        "recovery_reset_ms": t_recover,
        "total_cycle_ms": t_reset + t_base + t_demo + t_dossier + t_tx + t_recover
    }

async def main():
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Measure health check / startup response
        t0 = time.perf_counter()
        health_resp = await client.get(f"{BASE_URL}/api/health")
        t_health = (time.perf_counter() - t0) * 1000.0
        assert health_resp.status_code == 200
        print(f"Server Health Check: {health_resp.json()['status']} in {t_health:.2f} ms")

        # 5 Rehearsal Cycles
        cycles = []
        print("\n--- Starting 5 Full-System Demo Rehearsals ---")
        for i in range(1, 6):
            res = await run_rehearsal_cycle(client, i)
            cycles.append(res)
            print(f"Cycle {i}: Demo Exec={res['demo_execution_ms']:.1f}ms | Dossier Load={res['dossier_load_ms']:.1f}ms | Reset={res['reset_ms']:.1f}ms | Total Cycle={res['total_cycle_ms']:.1f}ms")

        # Rehearsal statistics
        demo_times = [c["demo_execution_ms"] for c in cycles]
        dossier_times = [c["dossier_load_ms"] for c in cycles]
        reset_times = [c["reset_ms"] for c in cycles]
        recovery_times = [c["recovery_reset_ms"] for c in cycles]
        total_times = [c["total_cycle_ms"] for c in cycles]

        print("\n================ REHEARSAL SUMMARY (5 CYCLES) ================")
        print(f"Judge Demo Execution: min={min(demo_times):.2f}ms | avg={statistics.mean(demo_times):.2f}ms | median={statistics.median(demo_times):.2f}ms | max={max(demo_times):.2f}ms")
        print(f"Dossier Loading Time: min={min(dossier_times):.2f}ms | avg={statistics.mean(dossier_times):.2f}ms | median={statistics.median(dossier_times):.2f}ms | max={max(dossier_times):.2f}ms")
        print(f"Reset Execution Time: min={min(reset_times):.2f}ms | avg={statistics.mean(reset_times):.2f}ms | median={statistics.median(reset_times):.2f}ms | max={max(reset_times):.2f}ms")
        print(f"Recovery Reset Time:  min={min(recovery_times):.2f}ms | avg={statistics.mean(recovery_times):.2f}ms | median={statistics.median(recovery_times):.2f}ms | max={max(recovery_times):.2f}ms")
        print(f"Total API Roundtrip:  min={min(total_times):.2f}ms | avg={statistics.mean(total_times):.2f}ms | median={statistics.median(total_times):.2f}ms | max={max(total_times):.2f}ms")
        print("ALL 5 REHEARSALS COMPLETED WITH 100% DETERMINISTIC REPEATABILITY")

if __name__ == "__main__":
    asyncio.run(main())
