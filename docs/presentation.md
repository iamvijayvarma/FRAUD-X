# FRAUD-X: Context-Aware Real-Time Financial Fraud Intelligence
## 24-Hour Hackathon Presentation Deck (FC-05)

---

### Slide 1: Title
**FRAUD-X**  
*Real-Time Context-Aware Financial Fraud Intelligence*  
**Problem Statement:** FC-05 — Real-Time Financial Fraud Detection Engine  
**Environment:** Synthetic Hackathon Data (Indian Financial Ecosystem — ₹ INR, UPI, IMPS, Domestic Banks)  
**Presenter Team:** Lead Software Architect & Full-Stack Engineering Team  

---

### Slide 2: The Problem — Why Isolated Transactions Miss Fraud
- **The Core Blindspot:** Traditional fraud systems evaluate financial transactions as isolated, discrete events.
- **The Reality of Modern Fraud:** Sophisticated threat actors never trigger naive single-transaction thresholds. Instead, fraud emerges progressively:
  $$\text{Normal Baseline} \longrightarrow \text{New Device} \longrightarrow \text{Unusual City} \longrightarrow \text{High-Value Push} \longrightarrow \text{Rapid Drains} \longrightarrow \text{Mule Network Link}$$
- **Example:** A ₹35,000 UPI transfer from a new phone in the customer's hometown might look acceptable on its own. When followed 8 minutes later by an ₹85,000 IMPS transfer from a city 1,000 km away, it is unmistakably an account takeover in progress.
- **Problem Statement (FC-05):** We must detect suspicious financial behaviour using **broader context** rather than evaluating transactions in isolation.

---

### Slide 3: The Existing Gap
> *"Transaction-centric detection can miss relationships and behavioural evolution that become visible only when multiple contextual signals are analysed together."*

- **Point-in-Time Blindness:** Stateless rules evaluate only: `IF amount > threshold THEN flag`. They lack memory of the account's historical baseline and trajectory.
- **Siloed Signal Processing:** Geolocation, device fingerprinting, velocity counters, and graph topologies are often processed in disconnected subsystems.
- **Lack of Narrative:** Existing engines produce opaque risk numbers (e.g. `Score: 78.4`) with no causal explanation of how the fraud unfolded over time.

---

### Slide 4: The FRAUD-X Solution Pipeline
FRAUD-X models fraud not as a point-in-time anomaly, but as an **evolving contextual event**:

$$\begin{aligned}
\text{Transaction Ingestion} &\longrightarrow \text{Context Retrieval (History, Devices, Geo)} \\
&\longrightarrow \text{Multi-Engine Detection (Behavioral, Device, Geo, Velocity, Graph, ML)} \\
&\longrightarrow \text{Risk Fusion & Hard Safety Overrides} \\
&\longrightarrow \text{Contextual Fraud Evolution & Change-Point Detection} \\
&\longrightarrow \text{Quantified Causal Evidence Engine} \\
&\longrightarrow \text{AI Forensic Analyst (Deterministic Fallback)} \\
&\longrightarrow \text{Action Recommendation (ALLOW, MONITOR, VERIFY, HOLD, BLOCK)}
\end{aligned}$$

---

### Slide 5: System Architecture
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER (React + Vite + Tailwind)             │
│  Live Command Center │ Investigation Drawer │ Graph View │ Judge Demo Runner│
└──────────────────────────────────────▲──────────────────────────────────────┘
                                       │ WebSocket (/ws/live) & REST (/api/v1)
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

### Slide 6: The Innovation — System-Level Contextual Integration
> **Important:** We do *not* claim that Isolation Forest, graph traversal, or velocity counters themselves are novel algorithms. Our innovation is the **system-level contextual architecture** that combines these signals into an evolving fraud narrative:

1. **Temporal Risk Evolution:** Tracks the velocity and acceleration of risk across an account's recent transaction window ($R_t - R_{t-1}$).
2. **Signal Confluence:** Quantifies how many independent risk dimensions (Device, Geo, Amount, Velocity, Network) fire concurrently.
3. **Cross-Entity Syndicate Correlation:** Propagates risk across accounts sharing hardware fingerprints or participating in circular fund transfers.
4. **Statistical Change-Point Detection:** Detects the exact inflection timestamp where account behaviour decoupled from its historical baseline.
5. **Causal Fraud Story Synthesis:** Automatically compiles raw signals into a human-readable forensic narrative.
6. **Adaptive Investigation Priority:** Ranks fraud cases into `URGENT`, `HIGH`, `ELEVATED`, and `ROUTINE` queues based on multi-vector confluence.

---

### Slide 7: The 30-Second Live Demo (5-Step Stepped Progression)
A deterministic, end-to-end evaluation flow on account `ACC-IN-1043`:
1. **Step 1: Normal Baseline** — ₹2,500 via UPI in Coimbatore $\rightarrow$ `Risk: 18 (LOW) | ALLOW`
2. **Step 2: Device Compromise** — ₹35,000 via new hardware fingerprint in Coimbatore $\rightarrow$ `Risk: 85 (ESCALATION) | CHALLENGE`
3. **Step 3: Geographic Anomaly** — ₹85,000 in Mumbai (3,960 km/h impossible travel speed) $\rightarrow$ `Risk: 80 (HIGH) | HOLD`
4. **Step 4: Rapid Drain** — ₹1,20,000 via IMPS in New Delhi $\rightarrow$ `Risk: 100 (CRITICAL) | BLOCK`
5. **Step 5: Syndicate Correlation** — Device linked to mule account `ACC-IN-1002` $\rightarrow$ `COORDINATED ATTACK FLAGGED`

*With 1-click instant deterministic Reset $\rightarrow$ Run $\rightarrow$ Reset repeatability.*

---

### Slide 8: Explainability & The Forensic Evidence Engine
**"WHY WAS THIS FLAGGED?"**
Every flagged transaction displays an un-fabricated, quantifiable evidence breakdown:
- **Observed Value:** Actual transaction metric (e.g. ₹1,20,000, 3,960 km/h, 4 tx/min).
- **Baseline Value:** Calibrated account historical norm (e.g. $\mu = ₹2,450 \pm ₹420$, known devices).
- **Point Contribution:** Exact mathematical weight contributed to the final risk score.
- **Forensic Narrative:** Cohesive English summary generated with 100% deterministic fallback (operates even if external LLM APIs are offline).

---

### Slide 9: Technology Stack
- **Frontend Workstation:** React 18, TypeScript, Vite, Tailwind CSS, Lucide Icons, Recharts.
- **Backend Service:** Python 3.11, FastAPI (Asynchronous), Pydantic v2 validation.
- **Database & Storage:** SQLite with aiosqlite in WAL mode (Optimized for local prototype demo).
- **Machine Learning:** Scikit-Learn Isolation Forest (unsupervised multi-dimensional anomaly detection).
- **Graph Engine:** NetworkX for in-memory directed graph modeling, circular cycle detection, and mule degree centrality.
- **Real-Time Streaming:** Native WebSocket hub (`/ws/live`) with bounded client-side ring buffers.
- **AI Analyst:** Dual-mode architecture (external LLM support with zero-latency deterministic forensic synthesizer).

---

### Slide 10: Impact & Production-Scale Roadmap
- **Current Prototype Capabilities:**
  - Sub-35ms contextual fraud evaluation pipeline.
  - Multi-engine risk fusion with hard safety overrides.
  - 100% localized to Indian payment rails (UPI, IMPS, NEFT, ₹ INR).
  - Repeatable judge demo with live simulated attacks and forensic drawer.
- **Production Architecture Roadmap:**
  - **Data Streaming:** Apache Kafka / Redis Streams for horizontally scalable ingestion.
  - **Distributed Database:** PostgreSQL with TimescaleDB for temporal partition queries.
  - **Graph Layer:** Managed Neo4j / Amazon Neptune for billion-edge syndicate graph traversal.
  - **Continuous Learning:** Scheduled model retraining pipelines with human-in-the-loop analyst feedback.
