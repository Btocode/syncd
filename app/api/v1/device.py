from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.device import DeviceSchema
from app.db.device_queries import (
    add_device,
    get_user_devices,
    get_device,
    update_device,
    delete_device
)
from app.core.security import get_current_user
from app.core.app_logging import logger
from app.db.database import get_session

router = APIRouter(prefix="/devices", tags=["Devices"])

@router.post("/", response_model=DeviceSchema)
async def register_device(
    device: DeviceSchema,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    try:
        device.user_id = current_user["id"]
        return await add_device(session, device)
    except Exception as e:
        logger.error(f"Error registering device: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[DeviceSchema])
async def get_user_devices_list(
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    try:
        return await get_user_devices(session, current_user["id"])
    except Exception as e:
        logger.error(f"Error getting user devices: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{device_id}", response_model=DeviceSchema)
async def update_device_info(
    device_id: str,
    device: DeviceSchema,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    try:
        existing_device = await get_device(session, device_id)
        if not existing_device or existing_device.user_id != current_user["id"]:
            raise HTTPException(status_code=404, detail="Device not found")
        return await update_device(session, device_id, device)
    except Exception as e:
        logger.error(f"Error updating device: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{device_id}")
async def remove_device(
    device_id: str,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    try:
        existing_device = await get_device(session, device_id)
        if not existing_device or existing_device.user_id != current_user["id"]:
            raise HTTPException(status_code=404, detail="Device not found")
        success = await delete_device(session, device_id)
        if not success:
            raise HTTPException(status_code=400, detail="Failed to delete device")
        return {"message": "Device deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting device: {e}")
        raise HTTPException(status_code=400, detail=str(e))
