from fastapi import APIRouter
from app.api.transactions import router as transactions_router
from app.api.analytics import router as analytics_router
from app.api.accounts import router as accounts_router
from app.api.graph import router as graph_router
from app.api.simulator import router as simulator_router
from app.api.ai import router as ai_router
from app.api.investigations import router as investigations_router

api_router = APIRouter()
api_router.include_router(transactions_router)
api_router.include_router(analytics_router)
api_router.include_router(accounts_router)
api_router.include_router(graph_router)
api_router.include_router(simulator_router)
api_router.include_router(ai_router)
api_router.include_router(investigations_router)

