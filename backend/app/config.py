from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "FRAUD-X Intelligence Engine"
    API_V1_STR: str = "/api"
    DATABASE_URL: str = "sqlite+aiosqlite:///./fraud_x.db"
    
    # LLM Settings
    OPENAI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    USE_MOCK_AI: bool = True
    
    # Engine Calibration Thresholds
    RISK_THRESHOLD_LOW: float = 30.0
    RISK_THRESHOLD_MEDIUM: float = 60.0
    RISK_THRESHOLD_HIGH: float = 85.0
    
    # Geo Intelligence
    IMPOSSIBLE_TRAVEL_SPEED_KMH: float = 800.0
    MIN_DISTANCE_FOR_TRAVEL_ALERT_KM: float = 100.0
    
    # Velocity Windows
    BURST_WINDOW_SECONDS: int = 60
    BURST_THRESHOLD_COUNT: int = 4
    CARD_TESTING_WINDOW_SECONDS: int = 300
    CARD_TESTING_THRESHOLD_COUNT: int = 7
    
    # Graph Engine
    MAX_SHARED_DEVICE_ACCOUNTS: int = 2
    
    model_config = {
        "env_file": ".env",
        "extra": "allow"
    }

settings = Settings()
