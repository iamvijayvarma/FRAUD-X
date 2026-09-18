# FRAUD-X: Quickstart & Setup Guide

This guide provides exact step-by-step instructions to reproduce and run the entire FRAUD-X platform from scratch on a clean environment.

---

## Prerequisites
- **Python**: 3.10+ (Tested on Python 3.11.9)
- **Node.js**: 18+ (Tested on Node.js v20+)
- **OS**: Windows, macOS, or Linux

---

## 1. Backend Setup & Startup

1. Open a terminal in `codebase/backend`:
   ```bash
   cd codebase/backend
   ```

2. Create and activate a Python virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Verify `.env` configuration (Default uses high-fidelity deterministic mock AI):
   ```env
   PROJECT_NAME="FRAUD-X Intelligence Engine"
   DATABASE_URL="sqlite+aiosqlite:///./fraud_x.db"
   USE_MOCK_AI=true
   ```

5. Run test suite to verify installation:
   ```bash
   python -m pytest tests -v
   ```
   *Expected: 13/13 tests pass in ~10–14 seconds.*

6. Start the FastAPI backend server:
   ```bash
   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
   ```
   *Health Check: Open `http://127.0.0.1:8000/api/health` $\rightarrow$ `{"status": "HEALTHY"}`.*

---

## 2. Frontend Setup & Startup

1. Open a second terminal in `codebase/frontend`:
   ```bash
   cd codebase/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Validate build:
   ```bash
   npm run build
   ```

4. Start the Vite development server:
   ```bash
   npm run dev -- --host 127.0.0.1 --port 5173
   ```

5. Open your browser to:
   ```
   http://127.0.0.1:5173
   ```

---

## 3. Running the Evaluator Demo

1. In the Command Center header, confirm that the green pulse indicates **"LIVE FEED CONNECTED"**.
2. Click the glowing amber **`JUDGE DEMO`** button in the top navigation.
3. Review the **"WHY FRAUD-X?"** innovation banner and the 5-step progression overview.
4. Click **`Run Judge Demo (30s Flow)`**.
5. Observe the 4 attack steps execute, culminating in a critical score of 100 on Step 4 and cross-account syndicate linking to `ACC-IN-1002`.
6. Click **`Reset`** to restore account `ACC-IN-1043` back to its clean 1-transaction baseline.
