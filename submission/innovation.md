# FRAUD-X: Innovation Architecture (FC-05)

## 1. The Core Innovation Thesis

The evaluator has raised the critical question:
> *"These algorithms already exist. What is your innovative approach?"*

Our answer:
> **"We do not claim that Isolation Forest, NetworkX, Haversine distance, or statistical Z-scores are novel in themselves. Our innovation is the SYSTEM-LEVEL ARCHITECTURE of Contextual Fraud Evolution — modeling fraud as an evolving, multi-dimensional event rather than an isolated transaction."**

---

## 2. The Five Pillars of Contextual Fraud Evolution

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                          CONTEXTUAL FRAUD EVOLUTION FORMULA                             │
│                                                                                         │
│  Temporal Behaviour + Signal Confluence + Cross-Entity Link + Change Detection + Story   │
│                                     ▼                                                   │
│                      CONTEXTUAL FRAUD EVOLUTION ENGINE                                  │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### Pillar 1: Temporal Risk Evolution ($R_t - R_{t-1}$)
Traditional fraud detection generates a point-in-time scalar score. FRAUD-X tracks the **first derivative (velocity)** and **second derivative (acceleration)** of risk across sliding temporal windows. An account transitioning from a risk of 18 to 85 within 10 minutes reflects a severe rate of change that triggers immediate investigation priority escalation.

### Pillar 2: Signal Confluence Index
Rather than summing linear heuristics, the engine evaluates the orthogonal confluence across 6 distinct intelligence dimensions:
- Behavioural Spending Z-score
- Device Hardware Fingerprint Novelty
- Geodesic Travel Velocity
- Sliding-Window Frequency Bursts
- Graph Ring Topology & Mule Links
- Unsupervised Isolation Forest Outlier Density

When 2 or more orthogonal signals activate concurrently, a compounding confluence multiplier elevates the risk level, preventing sophisticated attackers from staggering amounts to evade individual rule thresholds.

### Pillar 3: Real-Time Cross-Entity Syndicate Propagation
Single-account rules fail when a fraud ring operates across multiple accounts. When a rogue hardware fingerprint is detected across distinct bank accounts, the graph service immediately links the accounts in an active bipartite graph and propagates risk to connected nodes.

### Pillar 4: Statistical Change-Point Detection
Using sliding-window behavioral calibration, the engine identifies the exact inflection timestamp where an account's metrics (average spending, typical geographic cluster, transaction frequency) decoupled from historical norms, pinpointing the moment of credential compromise.

### Pillar 5: Explainable Causal Investigation Story
FRAUD-X produces a structured forensic evidence waterfall:
- **Observed Metric**: Exact transaction value (₹1,20,000, 3,960 km/h, 4 tx/min).
- **Baseline Metric**: Calibrated historical profile ($\mu = ₹2,450 \pm ₹420$, known hardware).
- **Point Attribution**: Mathematical contribution to the final risk score.
- **Narrative**: Cohesive English causal story generated with 100% resilient deterministic fallback.
