from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Device(Base):
    __tablename__ = "devices"

    id = Column(String(100), primary_key=True, index=True) # Device fingerprint hash
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)
    browser_os = Column(String(150), default="Chrome on macOS")
    is_known_proxy = Column(Boolean, default=False)
    risk_score = Column(Integer, default=0)

    account_links = relationship("AccountDevice", back_populates="device")
    transactions = relationship("Transaction", back_populates="device")


class AccountDevice(Base):
    __tablename__ = "account_devices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(String(50), ForeignKey("accounts.id"), index=True)
    device_id = Column(String(100), ForeignKey("devices.id"), index=True)
    first_used_at = Column(DateTime, default=datetime.utcnow)
    last_used_at = Column(DateTime, default=datetime.utcnow)
    usage_count = Column(Integer, default=1)

    account = relationship("Account", back_populates="device_links")
    device = relationship("Device", back_populates="account_links")
