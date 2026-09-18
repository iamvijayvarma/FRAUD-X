# FRAUD-X: Competition Submission Package (FC-05)

**Project:** FRAUD-X — Context-Aware Real-Time Financial Fraud Intelligence  
**Problem Statement:** FC-05 — Real-Time Financial Fraud Detection Engine  
**Environment:** Synthetic Hackathon Data (100% Indian Banking Ecosystem — ₹ INR, UPI, IMPS, Domestic Banks)  
**Status:** Feature Complete | 100% Test Pass (13/13) | Production Build Verified | Final Code Freeze  

---

## 📁 Submission Contents

- [`setup.md`](file:///c:/Users/vvarm/Downloads/JARVIS/codebase/submission/setup.md) — Step-by-step installation, dependency validation, and startup instructions.
- [`pitch.md`](file:///c:/Users/vvarm/Downloads/JARVIS/codebase/submission/pitch.md) — Spoken pitch scripts: 30-Second Elevator Pitch, 1-Minute Pitch, and 3-Minute Technical Presentation.
- [`demo-script.md`](file:///c:/Users/vvarm/Downloads/JARVIS/codebase/submission/demo-script.md) — Second-by-second live walkthrough script with exact actions and spoken lines.
- [`judge-qa.md`](file:///c:/Users/vvarm/Downloads/JARVIS/codebase/submission/judge-qa.md) — Comprehensive 20-question Judge Defense Sheet with Short and Deeper answers.
- [`innovation.md`](file:///c:/Users/vvarm/Downloads/JARVIS/codebase/submission/innovation.md) — Architectural breakdown answering the core evaluator challenge on system innovation.
- [`limitations.md`](file:///c:/Users/vvarm/Downloads/JARVIS/codebase/submission/limitations.md) — Transparent discussion of prototype scope and enterprise production roadmap.
- [`presentation.md`](file:///c:/Users/vvarm/Downloads/JARVIS/codebase/submission/presentation.md) — 10-slide hackathon presentation deck structure.
- [`demo/DEMO_GUIDE.md`](file:///c:/Users/vvarm/Downloads/JARVIS/codebase/submission/demo/DEMO_GUIDE.md) — Judge demo sequence and 60–90 second backup video recording plan.
- [`screenshots/`](file:///c:/Users/vvarm/Downloads/JARVIS/codebase/submission/screenshots/) — Complete library of 16 live UI screenshots captured during active testing.

---

## 🚀 Quick Verification
```bash
# 1. Backend tests
cd codebase/backend
python -m pytest tests -v
# Result: 13/13 PASSED in ~13s

# 2. Frontend production build
cd ../frontend
npm run build
# Result: Vite production build passed, 0 errors

# 3. Automated rehearsal benchmark
cd ../backend
python rehearsal_timing.py
# Result: 5 cycles, 100% deterministic repeatability, ~295ms demo execution
```
