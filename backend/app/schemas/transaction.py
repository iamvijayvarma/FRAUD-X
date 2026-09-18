from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from app.schemas.risk import RiskAssessment

class TransactionCreate(BaseModel):
    account_id: str # e.g. ACC-IN-1001
    amount: float = Field(..., gt=0.0) # In INR ₹
    currency: str = "INR"
    merchant_name: str = "Flipkart Online"
    merchant_category: str = "E-COMMERCE"
    transaction_type: str = "UPI" # UPI, Debit Card, Credit Card, Net Banking, IMPS, NEFT, POS, QR Payment
    target_account_id: Optional[str] = None
    bank_name: Optional[str] = "HDFC Bank"
    
    # Device context
    device_id: str # e.g. DEV-IN-XXXX
    ip_address: str = "103.21.244.10"
    
    # Geo context
    location_city: str = "Bengaluru"
    location_country: str = "India"
    location_lat: float = 12.9716
    location_lon: float = 77.5946
    
    # Optional client timestamp override
    timestamp: Optional[datetime] = None

class TransactionResponse(BaseModel):
    id: str
    timestamp: datetime
    account_id: str
    target_account_id: Optional[str] = None
    amount: float
    currency: str = "INR"
    merchant_name: str
    merchant_category: str
    transaction_type: str
    bank_name: Optional[str] = "HDFC Bank"
    device_id: str
    ip_address: str
    location_city: str
    location_country: str
    location_lat: float
    location_lon: float
    risk_score: float
    risk_level: str
    action_taken: str
    assessment: Optional[RiskAssessment] = None
    ai_narrative: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class TransactionListResponse(BaseModel):
    total: int
    transactions: List[TransactionResponse]
