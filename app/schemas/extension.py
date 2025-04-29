from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ExtensionBase(BaseModel):
    name: str
    enabled: bool = True
    version: str
    enable_link: Optional[str] = None
    disable_link: Optional[str] = None

class ExtensionCreate(ExtensionBase):
    pass

class ExtensionUpdate(ExtensionBase):
    pass

class ExtensionSchema(ExtensionBase):
    extension_id: str
    device_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True