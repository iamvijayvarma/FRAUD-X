# FRAUD-X: Top 15 Rapid-Fire Judge Questions (5s & 30s Answers)

This rapid-fire sheet equips the presenter to answer quickly in 5 seconds and seamlessly expand to a 30-second technical answer if pressed.

---

### 1. What problem are you solving?
- **5-Second Answer:** Detecting multi-step financial fraud schemes that traditional stateless transaction rules miss.
- **30-Second Answer:** Attackers don't steal money in one massive transaction anymore; they stagger amounts, rotate devices, and jump geographies. Traditional rules evaluate each transaction in isolation and miss the pattern. FRAUD-X evaluates the broader context across time, entities, and devices to catch attacks as they evolve.

---

### 2. What is your core innovation?
- **5-Second Answer:** System-level Contextual Fraud Evolution combining temporal acceleration, signal confluence, and cross-account links.
- **30-Second Answer:** We don't claim to invent Isolation Forest or graph traversals. Our innovation is the system-level architecture that tracks the rate of change of risk over time, requires multi-vector confluence before escalating, and automatically generates an explainable causal story with zero hallucination.

---

### 3. How does this differ from a standard fraud score?
- **5-Second Answer:** A score is a static scalar; FRAUD-X provides a temporal trajectory, change-point inflection, and causal evidence.
- **30-Second Answer:** A score of "85" doesn't tell an investigator *why* or *how* the account was compromised. FRAUD-X shows the acceleration from baseline, the exact change-point timestamp, the orthogonal confluence index, and links to connected mule devices.

---

### 4. Why use Isolation Forest instead of supervised learning?
- **5-Second Answer:** It catches zero-day anomalies without needing labeled historical fraud datasets.
- **30-Second Answer:** Supervised models suffer from severe concept drift when attacker tactics shift. Isolation Forest isolates anomalies in multi-dimensional space (Z-scores, velocity, speed, device reuse) without prior labels, serving as an unsupervised safety net alongside deterministic rules.

---

### 5. Why use graph analysis?
- **5-Second Answer:** To expose circular fund layering and shared device mule syndicates that relational tables miss.
- **30-Second Answer:** Attackers often use one emulator farm to drain multiple accounts or route funds through circular loops ($A \to B \to C \to A$). Our graph service maintains real-time account-device bipartite linkages and detects closed cycles in memory.

---

### 6. How do you prevent false positives?
- **5-Second Answer:** Through multi-signal confluence—one isolated anomaly never triggers a critical block.
- **30-Second Answer:** If a user buys an expensive flight from their usual phone in their home city, amount is high, but device, location, and velocity are normal. Because the confluence index is 1, it triggers monitoring, not a block. Hard blocks require multiple orthogonal anomalies or physical impossibility.

---

### 7. How does real-time processing work?
- **5-Second Answer:** Asynchronous microservices pipeline executing multi-engine fusion in under 35 milliseconds.
- **30-Second Answer:** Our FastAPI backend processes transactions asynchronously. Database queries use indexed WAL SQLite, mathematical calculations (Haversine, Z-score) execute in microseconds, and ML inference takes $<2\text{ms}$, streaming live decisions over WebSockets.

---

### 8. What happens if the AI service fails?
- **5-Second Answer:** The system automatically falls back to an internal deterministic forensic synthesizer with zero latency.
- **30-Second Answer:** Explainability is completely decoupled from external LLM availability. If an external API errors or is unconfigured, our internal synthesizer extracts all signal evidence fields and compiles the full causal story with 100% deterministic reliability.

---

### 9. Why use synthetic data?
- **5-Second Answer:** To safely demonstrate real-time fraud workflows without violating banking privacy regulations.
- **30-Second Answer:** Real customer banking logs are legally protected PII. We engineered a high-fidelity synthetic Indian financial dataset featuring domestic payment rails (UPI, IMPS), Indian Rupee distributions, and authentic multi-step attack sequences.

---

### 10. How would you scale this in production?
- **5-Second Answer:** Migrate ingestion to Apache Kafka, feature caching to Redis, and graph storage to Neo4j.
- **30-Second Answer:** The prototype uses SQLite and NetworkX for local demo portability. In production, transaction streams partition across Kafka topics, account history is served from Redis/Feast feature stores, and graph traversals are offloaded to distributed Neo4j clusters.

---

### 11. Can an attacker evade your system?
- **5-Second Answer:** Attackers can attempt low-and-slow probing, but temporal change-point detection raises their attack cost dramatically.
- **30-Second Answer:** If an attacker slowly increases transaction amounts, our sliding-window change-point detector catches the cumulative drift. If they rotate accounts, our device fingerprint graph links them. Evading completely would require months of slow micro-transactions from a unique legitimate device.

---

### 12. How does explainability work?
- **5-Second Answer:** Every point in the risk score is mathematically attributed to a specific signal evidence card.
- **30-Second Answer:** The forensic drawer renders an evidence waterfall comparing observed values directly against calibrated historical baselines, showing the exact point weight contributed by each vector (Amount, Device, Geo, Velocity, Graph, ML).

---

### 13. How do you detect coordinated syndicate activity?
- **5-Second Answer:** By mapping shared hardware fingerprints and tracking circular fund routing topologies.
- **30-Second Answer:** When multiple accounts authenticate from the same physical device fingerprint, our graph service builds edges between them. If device degree exceeds 2, `SUSPICIOUS_DEVICE_REUSE` fires, propagating risk across all linked accounts.

---

### 14. What is your biggest limitation?
- **5-Second Answer:** Prototype uses in-memory graphs and local SQLite rather than distributed streaming clusters.
- **30-Second Answer:** NetworkX is memory-bound and SQLite does not support multi-master writes. Furthermore, without access to proprietary bank logs, thresholds are calibrated using domain heuristics rather than empirical ROC-AUC optimization.

---

### 15. How would you deploy this in a real bank?
- **5-Second Answer:** As a sidecar microservice ingesting from the payment switch and publishing decisions in under 50ms.
- **30-Second Answer:** Incoming payments from UPI/IMPS switches publish to a Kafka topic. Stateless containerized risk workers score the transaction against Redis account caches and emit a decision (ALLOW, CHALLENGE, BLOCK) before settlement.
