from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Dict
from app.schemas.extension import ExtensionSchema
from app.db.models import DeviceStatus

class ExtensionsCount(BaseModel):
    enabled: int = 0
    disabled: int = 0
    total: int = 0

class DeviceBase(BaseModel):
    device_name: str
    device_type: str
    os_name: str
    os_version: str
    browser_name: Optional[str] = None
    browser_version: Optional[str] = None
    sync_enabled: bool = True
    terminal_configured: bool = False
    theme_configured: bool = False
    is_active: bool = True

class DeviceCreate(DeviceBase):
    pass

class DeviceUpdate(DeviceBase):
    pass

class DeviceSchema(DeviceBase):
    device_id: str
    user_id: str
    last_synced: datetime
    sync_status: DeviceStatus
    extensions: List[ExtensionSchema] = []
    extensions_count: ExtensionsCount

    @property
    def id(self) -> str:
        """Alias for device_id to match TypeScript interface"""
        return self.device_id

    @property
    def name(self) -> str:
        """Alias for device_name to match TypeScript interface"""
        return self.device_name

    @property
    def type(self) -> str:
        """Alias for device_type to match TypeScript interface"""
        return self.device_type

    @property
    def status(self) -> str:
        """Alias for sync_status to match TypeScript interface"""
        return self.sync_status.value

    @property
    def lastSynced(self) -> str:
        """Format last_synced as string to match TypeScript interface"""
        return self.last_synced.isoformat()

    class Config:
        from_attributes = True

    def dict(self, *args, **kwargs):
        """Override dict method to include computed properties"""
        d = super().dict(*args, **kwargs)
        d.update({
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "status": self.status,
            "lastSynced": self.lastSynced,
        })
        return d
