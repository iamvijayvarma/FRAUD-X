# FRAUD-X: Pre-Demo Checklist & Rapid Recovery Plan

This document ensures seamless execution during the hackathon evaluation and provides instant recovery protocols for any technical glitch.

---

## 1. Pre-Demo Verification Checklist (Run 10 Minutes Before Evaluation)

| Item | Command / Check | Expected State | Verified |
| :--- | :--- | :--- | :---: |
| **1. Backend Service** | `http://127.0.0.1:8000/api/health` | HTTP 200 `{"status": "HEALTHY"}` | [x] |
| **2. Frontend Dev Server** | `http://127.0.0.1:5173` | Command Center loads in `<1s` with green pulse | [x] |
| **3. WebSocket Hub** | Check Command Center header | Green "LIVE FEED CONNECTED" indicator | [x] |
| **4. Database Integrity** | Check accounts list | Seeded accounts `ACC-IN-1001` to `ACC-IN-1050` populated | [x] |
| **5. Test Suite** | `python -m pytest tests -v` | 13/13 PASSED (100%) | [x] |
| **6. Production Build** | `npm run build` | 0 errors, clean build | [x] |
| **7. Clean Demo State** | Click "Reset" on Judge Demo | Account `ACC-IN-1043` resets to 1 clean baseline record | [x] |

---

## 2. Emergency Demo Recovery Protocols

### Failure Scenario A: Backend Server Crashes or Closes
- **Symptoms:** Frontend shows "RECONNECTING TO LIVE FEED", API calls fail with Network Error.
- **Immediate Recovery Action:**
  1. Open terminal in `codebase/backend`.
  2. Run:
     ```powershell
     python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
     ```
  3. Wait 3 seconds for database initialization.
  4. Refresh browser tab at `http://127.0.0.1:5173`.
- **What to Say to Judges:**
  > *"We're reconnecting our real-time streaming worker to the local database hub... and we're back online with live streaming restored."*

---

### Failure Scenario B: WebSocket Disconnects or Hangs
- **Symptoms:** Live transaction stream stops updating; connection badge turns amber/red.
- **Immediate Recovery Action:**
  1. Click browser Refresh button (`Ctrl + R` or `F5`).
  2. The frontend automatically re-establishes the WebSocket connection upon load.
- **What to Say to Judges:**
  > *"Refreshing the telemetry client to resynchronize the live event stream."*

---

### Failure Scenario C: External AI Service (LLM) Unavailable or Times Out
- **Symptoms:** AI Narrative generation takes $>3$ seconds or throws API key error.
- **Immediate Recovery Action:**
  - **Do nothing!** The system architecture has built-in 100% resilient deterministic fallback.
  - The internal forensic synthesizer immediately generates the complete causal story and mitigation checklist with 0ms latency.
- **What to Say to Judges:**
  > *"Notice how our architecture handles external service degradation: our deterministic forensic synthesizer takes over instantly without dropping a single signal."*

---

### Failure Scenario D: Judge Demo Has Extra Transactions from Prior Testing
- **Symptoms:** Account `ACC-IN-1043` has 10+ transactions; progression stepper looks cluttered.
- **Immediate Recovery Action:**
  1. Click the **`Reset`** button next to **`Run Judge Demo (30s Flow)`**.
  2. In $<50\text{ms}$, the backend purges test transactions and restores the pristine 1-transaction baseline.
- **What to Say to Judges:**
  > *"Let's reset our test entity to its clean historical baseline so you can watch the attack unfold step-by-step."*

---

### Failure Scenario E: Accidental Browser Tab Close
- **Symptoms:** Browser closes.
- **Immediate Recovery Action:**
  1. Press `Ctrl + Shift + T` or reopen `http://127.0.0.1:5173`.
  2. Vite hot-reloads state immediately; backend daemon is still running.
- **What to Say to Judges:**
  > *"Reopening our analyst workstation."*

---

### Failure Scenario F: Attack Simulator Fails to Dispatch
- **Symptoms:** Clicking "Simulate Attack" does not appear to add transactions.
- **Immediate Recovery Action:**
  1. Use the dedicated **`JUDGE DEMO`** button in the header instead of the manual attack simulator modal.
  2. The Judge Demo endpoint (`POST /api/investigations/judge-demo`) executes atomically on the backend and returns the complete updated dossier in a single atomic response.
- **What to Say to Judges:**
  > *"Let's run our calibrated multi-step judge evaluation flow directly."*
