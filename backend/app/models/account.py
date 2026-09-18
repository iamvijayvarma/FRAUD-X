from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Account(Base):
    __tablename__ = "accounts"

    id = Column(String(50), primary_key=True, index=True) # e.g. ACC-IN-1001
    holder_name = Column(String(100), nullable=False)
    email = Column(String(120), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Historical Behavioral Baselines (in INR ₹)
    avg_amount = Column(Float, default=3500.0)
    std_amount = Column(Float, default=950.0)
    typical_city = Column(String(100), default="Coimbatore")
    typical_country = Column(String(50), default="India")
    typical_location_lat = Column(Float, default=11.0168)
    typical_location_lon = Column(Float, default=76.9558)
    primary_bank = Column(String(50), default="HDFC Bank") # Synthetic label
    
    # Account Status
    status = Column(String(30), default="ACTIVE") # ACTIVE, SUSPENDED, FROZEN, UNDER_REVIEW
    risk_rating = Column(String(20), default="LOW") # LOW, MEDIUM, HIGH, CRITICAL

    transactions = relationship("Transaction", back_populates="account", foreign_keys="Transaction.account_id")
    device_links = relationship("AccountDevice", back_populates="account")
