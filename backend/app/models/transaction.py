from sqlalchemy import Column, String, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String(50), primary_key=True, default=lambda: f"TXN-IN-{uuid.uuid4().hex[:8].upper()}", index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Financial & Institution Identifiers
    account_id = Column(String(50), ForeignKey("accounts.id"), index=True, nullable=False)
    target_account_id = Column(String(50), nullable=True) # For P2P / IMPS / UPI transfers
    
    # Financial details
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="INR")
    merchant_name = Column(String(150), default="Flipkart Retail")
    merchant_category = Column(String(100), default="E-COMMERCE")
    transaction_type = Column(String(50), default="UPI") # UPI, Debit Card, Credit Card, Net Banking, IMPS, NEFT, POS, QR Payment
    bank_name = Column(String(50), default="HDFC Bank") # Contextual synthetic label: SBI, HDFC Bank, ICICI Bank, Axis Bank
    
    # Contextual Attributes
    device_id = Column(String(100), ForeignKey("devices.id"), nullable=False)
    ip_address = Column(String(50), default="103.21.244.10")
    location_city = Column(String(100), default="Bengaluru")
    location_country = Column(String(50), default="India")
    location_lat = Column(Float, default=12.9716)
    location_lon = Column(Float, default=77.5946)
    
    # Intelligence Outcomes
    risk_score = Column(Float, default=0.0) # 0.0 - 100.0
    risk_level = Column(String(20), default="LOW") # LOW, MEDIUM, HIGH, CRITICAL
    action_taken = Column(String(30), default="ALLOW") # ALLOW, MONITOR, CHALLENGE, HOLD, BLOCK
    
    # Evidence & Explainability Payload
    evidence_json = Column(Text, nullable=True)
    ai_narrative = Column(Text, nullable=True)
    
    is_synthetic = Column(Boolean, default=True)

    # Relationships
    account = relationship("Account", back_populates="transactions", foreign_keys=[account_id])
    device = relationship("Device", back_populates="transactions")
    alerts = relationship("Alert", back_populates="transaction")
