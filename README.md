# FRAUD-X: Real-Time Context-Aware Financial Fraud Intelligence
### Problem Statement FC-05: Real-Time Financial Fraud Detection Engine

> **Environment:** Synthetic Hackathon Prototype (Indian Financial Ecosystem — ₹ INR, UPI, IMPS, Domestic Banks)  
> **Status:** Final Competition Freeze | 13/13 Pytest Suite Passed | Vite Build Passed (0 Errors)

---

## 1. Project Overview
**FRAUD-X** is an enterprise-grade real-time financial fraud intelligence engine and analyst command workstation engineered to address **Problem Statement FC-05**. Rather than evaluating transactions as isolated events, FRAUD-X tracks how suspicious behaviour **evolves over time**, detects **confluent multi-dimensional signals**, links **cross-account fraud rings**, and produces **quantifiable, explainable forensic evidence** with recommended mitigation actions in real time.

---

## 2. The Problem: The Isolated Transaction Blindspot
Traditional banking fraud systems evaluate financial transactions as stateless, isolated events:
$$\text{IF Amount } > \text{ Threshold THEN Flag}$$
Modern financial attackers exploit this blindspot. Sophisticated fraud unfolds across a multi-step compromise timeline:
1. **Reconnaissance & Device Compromise:** Pairing a new hardware fingerprint with stolen credentials.
2. **Geographic Hopping:** Routing transactions from remote cities using VPNs or SIM-swap exploits.
3. **Pacing Below Thresholds:** Initiating moderate-value transfers (e.g. ₹35,000, ₹85,000) that individually evade single-transaction limits.
4. **Rapid Capital Flight:** Draining remaining liquidity via instant payment rails (UPI / IMPS).
5. **Syndicate Layering:** Dispersing funds into coordinated money-mule accounts sharing the same attack device.

Evaluated in isolation, each transaction appears legitimate. Evaluated in context, it is unmistakably an attack in progress.

---

## 3. The Solution
FRAUD-X re-architects fraud detection into an **evolving contextual event**:
$$\begin{aligned}
\text{Transaction} &\longrightarrow \text{Context Retrieval} \longrightarrow \text{Modular Intelligence Engines} \\
&\longrightarrow \text{Risk Fusion & Hard Overrides} \longrightarrow \text{Temporal Evolution & Change-Point} \\
&\longrightarrow \text{Forensic Evidence Waterfall} \longrightarrow \text{AI Forensic Analyst} \longrightarrow \text{Action}
\end{aligned}$$

---

## 4. The System Innovation
> **Important:** We do *not* claim that Isolation Forest, graph analysis, or Haversine distance are novel algorithms in themselves. Our innovation is the **system-level architecture of Contextual Fraud Evolution**:

- **Temporal Risk Evolution ($R_t - R_{t-1}$):** Continuously tracks the velocity and acceleration of risk across an account's recent transaction trajectory.
- **Signal Confluence Index:** Compounding risk multiplier when orthogonal signals (Device + Location + Velocity + Graph + ML) fire concurrently.
- **Cross-Entity Syndicate Propagation:** Real-time graph linking of accounts sharing hardware fingerprints or participating in circular fund transfers.
- **Statistical Change-Point Detection:** Pinpoints the exact inflection timestamp where account telemetry decoupled from its historical baseline.
- **Explainable Causal Investigation Story:** Reconstructs the complete attack narrative with 100% deterministic fallback and zero hallucination.
- **Adaptive Investigation Priority:** Automatically triages cases into `URGENT`, `HIGH`, `ELEVATED`, and `ROUTINE` queues.

---

## 5. System Architecture
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER (React 18 + Vite + Tailwind)          │
│  Live Command Center │ Investigation Drawer │ Graph View │ Judge Demo Runner│
└──────────────────────────────────────▲──────────────────────────────────────┘
                                       │ WebSocket (/ws/live) & REST (/api)
┌──────────────────────────────────────┴──────────────────────────────────────┐
│                  INVESTIGATION & FORENSIC INTELLIGENCE LAYER                │
│   Contextual Evolution Dossier │ Change-Point Engine │ AI Forensic Analyst  │
└──────────────────────────────────────▲──────────────────────────────────────┘
                                       │ Multi-Dimensional Evidence Waterfall
┌──────────────────────────────────────┴──────────────────────────────────────┐
│                    RISK FUSION & CONTEXTUAL EVOLUTION LAYER                 │
│      Heuristic Fusion │ Safety Overrides │ Temporal Trajectory Tracking     │
└──────────────────────────────────────▲──────────────────────────────────────┘
                                       │ Raw Risk Signals & Features
┌──────────────────────────────────────┴──────────────────────────────────────┐
│                      MODULAR DETECTION ENGINE LAYER                         │
│  Behavioral Z-Score │ Device Fingerprint │ Haversine Velocity │ Burst Engine │
│  Isolation Forest ML │ NetworkX Graph Topology & Mule Ring Detector        │
└──────────────────────────────────────▲──────────────────────────────────────┘
                                       │ Account History, Device Links, Baseline
┌──────────────────────────────────────┴──────────────────────────────────────┐
│                      DATA & CONTEXT INFRASTRUCTURE                          │
│        FastAPI Async Backend │ SQLite (WAL Mode) │ Seeded Baseline Data     │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Technology Stack
- **Frontend:** React 18, TypeScript, Vite, Tailwind CSS, Lucide React, Recharts.
- **Backend:** Python 3.11, FastAPI (Asynchronous), Pydantic v2.
- **Database:** SQLite with aiosqlite in WAL mode (Optimized for local prototype demo).
- **Machine Learning:** Scikit-Learn Isolation Forest (unsupervised multi-dimensional anomaly detection).
- **Graph Engine:** NetworkX for in-memory bipartite account-device graphs and circular loop detection.
- **Real-Time Streaming:** Native WebSocket hub (`/ws/live`) with bounded client-side ring buffers.
- **Explainability:** Dual-mode AI Analyst (external LLM support with zero-latency deterministic forensic synthesizer).

---

## 7. Key Features
1. **Live Command Center:** Real-time KPI counters, streaming transaction feed, and interactive entity drawer.
2. **Forensic Evidence Waterfall:** "WHY WAS THIS FLAGGED?" card displaying exact observed metrics vs historical baselines and point weights.
3. **Contextual Evolution Dossier:** Temporal risk trajectory graph, change-point inflection detection, and cross-account syndicate mapping.
4. **Deterministic Judge Demo:** 5-step stepped progression with instant 1-click **Reset** for multi-cycle repeatable evaluation.
5. **Attack Simulator:** Interactive injector to simulate burst velocity, impossible travel, and syndicate attacks on demand.

---

## 8. Indian Financial Ecosystem Localization
- **Currency:** Indian Rupees (`₹` / INR) with authentic formatting (e.g. ₹2,450, ₹1,20,000) across all UI screens and backend APIs.
- **Payment Rails:** UPI, IMPS, NEFT, Net Banking, Debit Card, Credit Card, QR Payment.
- **Domestic Institutions:** HDFC Bank, ICICI Bank, State Bank of India, Axis Bank, Kotak Mahindra Bank.
- **Realistic Cities & Merchant Ecosystem:** Coimbatore, Bengaluru, Mumbai, New Delhi, Chennai, Hyderabad; Swiggy, Zomato, Flipkart, Amazon India, IRCTC.

---

## 9. Testing & Empirical Verification
- **Pytest Suite:** 13/13 tests passing (100%) in `13.49s`.
- **Frontend Build:** `npm run build` passes with 0 errors in `15.53s`.
- **Rehearsal Benchmark (5 Consecutive Cycles):**
  - Judge Demo Execution: **293.14 ms median** (min: 286.02ms, max: 313.38ms)
  - Investigation Dossier Loading: **30.98 ms median** (min: 28.51ms, max: 32.92ms)
  - Reset Execution: **94.94 ms median** (min: 93.31ms, max: 97.53ms)
  - Total API Roundtrip: **552.29 ms median** (min: 544.75ms, max: 572.10ms)
  - Multi-Cycle Repeatability: **100% deterministic**

---

## 10. Known Limitations & Prototype Scope
- **Synthetic Data:** Uses synthetic Indian transaction data rather than proprietary customer bank logs.
- **In-Memory Graph:** NetworkX is suitable for prototype scale; production deployment maps to Neo4j.
- **Local SQLite:** WAL mode is optimized for local evaluation; enterprise deployment maps to PostgreSQL + TimescaleDB.
- **Scope:** Produces **System Recommendations** (ALLOW, MONITOR, VERIFY, HOLD, BLOCK); does not claim real statutory regulatory integration.

---

## 11. Production Roadmap
- **Streaming:** Apache Kafka / Redis Streams for horizontally scalable 50,000+ TPS ingestion.
- **Distributed Database:** PostgreSQL with TimescaleDB for partition-pruned temporal queries.
- **Enterprise Graph:** Managed Neo4j or Amazon Neptune for real-time billion-edge syndicate traversal.
- **Security:** Mutual TLS (mTLS), PAN Tokenization, AES-256 encryption, and strict RBAC.

---

## 12. Setup Instructions

### Backend:
```bash
cd codebase/backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python -m pytest tests -v
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### Frontend:
```bash
cd codebase/frontend
npm install
npm run build
npm run dev -- --host 127.0.0.1 --port 5173
```
Open `http://127.0.0.1:5173` in your browser.
