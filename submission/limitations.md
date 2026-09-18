# FRAUD-X: Known Limitations & Production Scalability Blueprint

In accordance with hackathon evaluation guidelines, this document provides an honest, transparent overview of current prototype limitations and the architectural roadmap required for tier-1 enterprise banking deployment.

---

## 1. Prototype Scope & Known Limitations

### A. Data & Benchmark Limitations
- **Synthetic Data vs. Real Banking Logs:** All accounts, transactions, and devices in FRAUD-X are high-fidelity synthetic records. While calibrated to authentic Indian payment distributions (₹ INR, UPI, domestic cities), the system has not been validated on real, proprietary bank datasets due to privacy regulations and lack of access to labeled production banking logs.
- **No ROC-AUC / Precision-Recall Benchmark Claims:** We do *not* claim a specific statistical accuracy percentage (e.g. "99.8% precision") because empirical accuracy metrics require a standardized, multi-million transaction benchmark dataset with verified chargeback ground truth.

### B. Storage & In-Memory Concurrency
- **SQLite Database:** The prototype uses SQLite with `aiosqlite` in WAL (Write-Ahead Logging) mode. While optimal for local hackathon demonstration and fast single-node queries, SQLite does not support high-concurrency multi-master horizontal write scaling.
- **In-Memory NetworkX Graph:** The graph intelligence engine uses NetworkX stored in process memory. While suitable for thousands of nodes in a demo, NetworkX is memory-bound and cannot handle the tens of millions of accounts and billion-edge topologies typical of enterprise card networks.

### C. Authentication & Authorization
- **Prototype Permissive Access:** To streamline hackathon evaluation and avoid friction during rapid judging, API endpoints and WebSocket channels are unauthenticated, and CORS is set to allow all origins in development mode.
- **No Real Regulatory Powers:** The platform produces **System Recommendations** (ALLOW, MONITOR, VERIFY, HOLD, BLOCK). It does not hold real-world statutory integration with RBI, NPCI, or FIU-IND systems.

---

## 2. Production Scalability & Migration Blueprint

To transition FRAUD-X from a verified hackathon prototype to an enterprise-grade banking intelligence platform handling 10,000+ transactions per second, the following architecture is specified:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PAYMENT GATEWAY / SWITCH (UPI, IMPS, CARDS)              │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ Raw Event Stream
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    INGESTION LAYER: APACHE KAFKA / REDIS STREAMS            │
│  Partitioned by Account ID Hash │ In-Order Partitioning │ 50,000+ TPS       │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ Parallel Consumer Group
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                  STATELESS RISK FUSION PODS (FastAPI / Go / Rust)           │
│  - Low-Latency Feature Retrieval via Redis / Feast Feature Store (<5ms)    │
│  - Parallel Modular Engine Execution (Z-Score, Geo-Velocity, Isolation ML) │
│  - Graph Query to Neo4j / Amazon Neptune Cluster (Mule Ring Cycles)         │
│  - Deterministic Safety Overrides & Dynamic Confluence Scoring              │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ Scored Decisions & Evidence JSON
                        ┌──────────────┴──────────────┐
                        ▼                             ▼
┌──────────────────────────────┐       ┌──────────────────────────────────────┐
│  PERSISTENCE: POSTGRESQL     │       │     ANALYST WEBSOCKET WORKSTATION    │
│  - TimescaleDB Partitioning  │       │  - Redis Pub/Sub Cluster             │
│  - Cold Storage in S3 Parquet│       │  - OAuth 2.0 / OIDC & Least-Privilege│
└──────────────────────────────┘       └──────────────────────────────────────┘
```

### Component Migration Map:
1. **Streaming:** SQLite sync $\longrightarrow$ **Apache Kafka / AWS Kinesis** topic partitioning.
2. **Feature Store:** Relational query lookup $\longrightarrow$ **Redis Cluster / Feast** with sub-5ms p99 read latency.
3. **Graph Database:** NetworkX $\longrightarrow$ **Neo4j Enterprise / Amazon Neptune** with Cypher pattern matching for circular rings.
4. **Relational Storage:** SQLite $\longrightarrow$ **PostgreSQL 16** with TimescaleDB extension for hypertable temporal indexing.
5. **Security:** Permissive dev mode $\longrightarrow$ **Mutual TLS (mTLS), PAN Tokenization, AES-256 field-level encryption**, and strict RBAC.
