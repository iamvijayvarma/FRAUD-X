# FRAUD-X: Judge Demo & Video Screen Recording Guide

---

## 1. Quick Rehearsal Overview (30 Seconds)

1. Open `http://127.0.0.1:5173`.
2. Verify top bar shows **`SYNTHETIC HACKATHON DATA`** and green **`LIVE FEED CONNECTED`**.
3. Click the glowing amber **`JUDGE DEMO`** button in the header.
4. Click **`Run Judge Demo (30s Flow)`**.
5. Observe the 5-step progression on account `ACC-IN-1043`:
   - Step 1: ₹2,500 via UPI in Coimbatore $\rightarrow$ LOW (18)
   - Step 2: ₹35,000 via New Device in Coimbatore $\rightarrow$ ESCALATION (85)
   - Step 3: ₹85,000 in Mumbai (Impossible Travel at 3,960 km/h) $\rightarrow$ HIGH (80)
   - Step 4: ₹1,20,000 in New Delhi via IMPS $\rightarrow$ CRITICAL (100)
   - Step 5: Cross-Account Syndicate Linking with `ACC-IN-1002` sharing `DEV-IN-SYNDICATE-ATTACK`.
6. Click **`Reset`** to restore the account to clean baseline.

---

## 2. 60–90 Second Backup Screen Recording Plan

If a live presentation cannot be conducted due to projector or network failure, use this recorded video sequence:

| Segment | Duration | Screen Action | Narration Focus |
| :--- | :--- | :--- | :--- |
| **1. Problem & Context** | 0:00 – 0:15 | Command Center Overview | Point out ₹ INR formatting, UPI rails, synthetic hackathon data badge, and explain why isolated transaction checks miss fraud. |
| **2. Launching Attack** | 0:15 – 0:35 | Click Judge Demo $\to$ Run Demo | Show the 5-step stepper activating sequentially; highlight the sudden risk velocity increase from Step 1 to Step 4. |
| **3. Risk Evolution Graph** | 0:35 – 0:50 | Focus on Trajectory Graph | Highlight the change-point detector identifying the exact moment of credential compromise at Step 2. |
| **4. Syndicate Network** | 0:50 – 1:05 | Scroll to Cross-Account Card | Show the bipartite link between `ACC-IN-1043` and `ACC-IN-1002` sharing rogue hardware. |
| **5. Causal Evidence** | 1:05 – 1:20 | Open Forensic Drawer | Point out the **"WHY WAS THIS FLAGGED?"** card with exact observed metrics vs calibrated historical baselines. |
| **6. Repeatability & Wrap**| 1:20 – 1:30 | Click Reset | Show instant return to baseline; conclude with the 35ms evaluation capability. |
