from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=True)  # nullable for social login
    display_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Add the missing relationship
    devices = relationship("Device", back_populates="user")

class DeviceStatus(str, enum.Enum):
    SYNCED = "synced"
    CHANGED = "changed"
    ERROR = "error"

class Device(Base):
    __tablename__ = "devices"

    device_id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    device_name = Column(String, nullable=False)
    device_type = Column(String, nullable=False)
    os_name = Column(String, nullable=False)
    os_version = Column(String, nullable=False)
    browser_name = Column(String, nullable=True)
    browser_version = Column(String, nullable=True)
    last_synced = Column(DateTime, default=datetime.utcnow)
    sync_status = Column(Enum(DeviceStatus), default=DeviceStatus.SYNCED)
    sync_enabled = Column(Boolean, default=True)
    terminal_configured = Column(Boolean, default=False)
    theme_configured = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="devices")
    extensions = relationship("Extension", back_populates="device", cascade="all, delete-orphan")

class Extension(Base):
    __tablename__ = "extensions"

    extension_id = Column(String, primary_key=True)
    device_id = Column(String, ForeignKey("devices.device_id"), nullable=False)
    name = Column(String, nullable=False)
    enabled = Column(Boolean, default=True)
    version = Column(String, nullable=False)
    enable_link = Column(String, nullable=True)
    disable_link = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    device = relationship("Device", back_populates="extensions")