# FRAUD-X: Pitch Scripts (30s, 1m, 3m)

---

## Pitch A: The 30-Second Elevator Pitch
*(Target duration: 25–30 seconds | Words: ~75)*

> "Traditional fraud detection evaluates financial transactions in isolation — which is why modern fraudsters bypass rules simply by keeping amounts moderate and staggering payments.
>
> **FRAUD-X** changes the paradigm: we model fraud as an **evolving contextual event**. By fusing temporal behavioural baselines, geolocation velocity, hardware fingerprints, and cross-account syndicate links in real time, FRAUD-X detects account takeovers and coordinated money-mule networks the moment they emerge.
>
> Instead of an opaque risk number, it delivers an actionable forensic story and clear intervention recommendations in under 35 milliseconds."

---

## Pitch B: The 1-Minute Pitch
*(Target duration: 55–60 seconds | Words: ~160)*

> "Judges, consider a typical financial fraud case. An attacker compromises a victim’s net banking credentials. Their first transaction is a modest ₹35,000 purchase from a new phone in the victim's hometown. A standard transaction rule approves it because the amount isn't massive.
>
> Ten minutes later, ₹85,000 is transferred from a city 1,000 kilometres away. Twenty minutes later, an IMPS transfer of ₹1,20,000 drains the account into a recipient account that shares that exact same rogue device.
>
> Evaluated individually, these look like ordinary payments. But evaluated in context, it is unmistakably an organized syndicate attack.
>
> This is **FRAUD-X** — built specifically for problem statement **FC-05**.
>
> We don't just score transactions; we track **Contextual Fraud Evolution**. Our engine continuously fuses behavioural deviation, physical transit velocity, hardware novelty, graph ring topology, and unsupervised ML into a single deterministic risk fusion pipeline.
>
> When fraud occurs, FRAUD-X pinpointed the exact inflection point, links connected mule accounts, and presents an explainable forensic evidence waterfall so human analysts can stop capital flight before it's too late."

---

## Pitch C: The 3-Minute Comprehensive Technical Pitch
*(Target duration: 2m 45s – 3m 00s | Words: ~450)*

> **[0:00 – 0:30 | The Core Problem & FC-05]**  
> "Good morning, judges. We are presenting **FRAUD-X**, built for Problem Statement **FC-05: Real-Time Financial Fraud Detection Engine**.
>
> Every year, millions in fraudulent transactions bypass banking filters. Why? Because the prevailing banking architecture evaluates transactions as isolated events. A rule checks: *'Is this transaction above the daily limit?'* If no, it passes.
>
> But modern financial crime doesn't work in isolation. Attackers operate across multi-step compromise timelines: credential harvesting, device pairing, test probes, geographic displacement, and rapid liquidity extraction across mule rings. To catch them, you need context."
>
> **[0:30 – 1:15 | The System Architecture & Multi-Engine Fusion]**  
> "FRAUD-X is engineered to evaluate the full context surrounding every single rupee transferred.
>
> When a transaction arrives through our high-speed API, our engine evaluates six independent intelligence dimensions simultaneously:
> 1. **Behavioural Profiling:** Calculates running statistical Z-scores against the account's historical spending mean and standard deviation.
> 2. **Device Intelligence:** Validates hardware fingerprint novelty and tracks device-to-account reuse ratios.
> 3. **Geodesic Travel Velocity:** Computes physical transit speed between consecutive transactions using the Haversine formula, flagging impossible speeds exceeding 800 km/h.
> 4. **Velocity Burst Tracking:** Sliding-window frequency counters that capture automated card testing and probe transactions.
> 5. **Graph Topology Analysis:** In-memory directed graph modeling that detects circular fund layering and mule accounts sharing hardware.
> 6. **Unsupervised ML Anomaly Detection:** An Isolation Forest model that evaluates multi-dimensional outlier densities without requiring labeled historical fraud."
>
> **[1:15 – 2:00 | The System Innovation: Contextual Fraud Evolution]**  
> "Now, you might ask: *'These algorithms exist. What is your innovation?'*
>
> Our innovation is not claiming to invent Isolation Forest or Haversine distance. Our innovation is the **system-level architecture of Contextual Fraud Evolution**.
>
> Rather than relying on static score thresholds, FRAUD-X tracks the **temporal acceleration of risk** across an account's trajectory. It computes a **Signal Confluence Index** across all six vectors, detects behavioural change-points where normal patterns decouple, and actively propagates risk to related accounts sharing hardware or routing circular funds.
>
> It transforms disconnected data into a coherent **Causal Fraud Story**."
>
> **[2:00 – 2:40 | The Live Demonstration & Explainability]**  
> "In our live command center, you can see this in action.
>
> In our 30-second Judge Demo on account `ACC-IN-1043`, you watch an account start at a completely normal baseline of ₹2,500 via UPI in Coimbatore. As the attack unfolds across a new device, an impossible jump to Mumbai, and a rapid drain to Delhi, FRAUD-X automatically catches the exact inflection point, escalates the priority to `URGENT`, and correlates the attack hardware directly to a known mule account `ACC-IN-1002`.
>
> Crucially, our system is completely explainable. The **'WHY WAS THIS FLAGGED?'** evidence waterfall displays exact observed values versus account baselines, mathematical point contributions, and recommended mitigation actions."
>
> **[2:40 – 3:00 | Conclusion & Impact]**  
> "FRAUD-X is fully localized to the Indian financial ecosystem with ₹ INR formatting, domestic banks, and UPI/IMPS rails. It runs end-to-end with sub-35ms evaluation latency and 100% resilient deterministic fallbacks.
>
> Thank you, and we are excited to walk you through the live system!"
