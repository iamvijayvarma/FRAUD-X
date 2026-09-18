from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.config import settings
from app.database import init_db, AsyncSessionLocal
from app.api import api_router
from app.websocket.connection_manager import manager
from app.utils.seed_data import seed_database
from app.services.graph_service import graph_service
from app.models.account import Account
from app.models.device import AccountDevice
from sqlalchemy import select

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("fraud_x.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup sequence
    logger.info("Initializing FRAUD-X Intelligence Engine...")
    await init_db()
    
    # Seed baseline data
    async with AsyncSessionLocal() as session:
        await seed_database(session)
        # Hydrate graph service with seeded accounts and device connections
        accs_res = await session.execute(select(Account))
        accounts = accs_res.scalars().all()
        for acc in accounts:
            graph_service.add_account(acc.id, acc.holder_name, risk_level=acc.risk_rating)

        links_res = await session.execute(select(AccountDevice))
        links = links_res.scalars().all()
        for link in links:
            graph_service.record_device_usage(link.account_id, link.device_id, link.last_used_at.isoformat())

    logger.info("FRAUD-X Engine ready for live streaming & simulation.")
    yield
    # Shutdown sequence
    logger.info("Shutting down FRAUD-X Engine...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Context-Aware Real-Time Financial Fraud Intelligence (FC-05)",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for React Vite frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount REST API
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {
        "system": settings.PROJECT_NAME,
        "status": "OPERATIONAL",
        "docs": "/docs",
        "health": "/api/health"
    }

@app.get("/api/health")
async def health_check():
    return {
        "status": "HEALTHY",
        "models": {
            "behavioral_engine": "ACTIVE",
            "device_intelligence": "ACTIVE",
            "location_velocity": "ACTIVE",
            "graph_engine": "ACTIVE",
            "isolation_forest_ml": "ACTIVE",
            "ai_analyst": "ACTIVE"
        },
        "connected_clients": len(manager.active_connections)
    }

@app.websocket("/ws/live")
async def websocket_endpoint(websocket: WebSocket):
    """Real-time bi-directional WebSocket hub for live transaction streaming."""
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive; accept any client messages/pings
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.warning(f"WebSocket error: {e}")
        manager.disconnect(websocket)
