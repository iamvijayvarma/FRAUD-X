from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.database import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(String(50), primary_key=True, default=lambda: f"ALT-{uuid.uuid4().hex[:8].upper()}", index=True)
    transaction_id = Column(String(50), ForeignKey("transactions.id"), index=True, nullable=False)
    account_id = Column(String(50), ForeignKey("accounts.id"), index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    risk_score = Column(Float, nullable=False)
    risk_level = Column(String(20), nullable=False) # HIGH, CRITICAL
    status = Column(String(30), default="OPEN") # OPEN, INVESTIGATING, DISMISSED, CONFIRMED_FRAUD
    
    summary = Column(String(255), nullable=False)
    ai_summary = Column(Text, nullable=True)
    analyst_notes = Column(Text, nullable=True)

    transaction = relationship("Transaction", back_populates="alerts")
