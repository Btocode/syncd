from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.schemas.device import DeviceSchema
from app.db.models import Device
from app.core.app_logging import logger

async def add_device(session: AsyncSession, device: DeviceSchema) -> DeviceSchema:
    try:
        db_device = Device(
            device_id=device.device_id,
            user_id=device.user_id,
            device_name=device.device_name,
            os_name=device.os_name,
            os_version=device.os_version,
            browser_name=device.browser_name,
            browser_version=device.browser_version,
            last_login=device.last_login,
            is_active=device.is_active
        )
        session.add(db_device)
        await session.commit()
        await session.refresh(db_device)
        return device
    except Exception as e:
        logger.error(f"Error adding device: {e}")
        await session.rollback()
        raise

async def get_user_devices(session: AsyncSession, user_id: str) -> list[DeviceSchema]:
    try:
        query = select(Device).where(Device.user_id == user_id)
        result = await session.execute(query)
        devices = result.scalars().all()
        return [
            DeviceSchema(
                device_id=device.device_id,
                user_id=device.user_id,
                device_name=device.device_name,
                os_name=device.os_name,
                os_version=device.os_version,
                browser_name=device.browser_name,
                browser_version=device.browser_version,
                last_login=device.last_login,
                is_active=device.is_active
            ) for device in devices
        ]
    except Exception as e:
        logger.error(f"Error getting user devices: {e}")
        raise

async def get_device(session: AsyncSession, device_id: str) -> DeviceSchema | None:
    try:
        query = select(Device).where(Device.device_id == device_id)
        result = await session.execute(query)
        device = result.scalar_one_or_none()
        if device:
            return DeviceSchema(
                device_id=device.device_id,
                user_id=device.user_id,
                device_name=device.device_name,
                os_name=device.os_name,
                os_version=device.os_version,
                browser_name=device.browser_name,
                browser_version=device.browser_version,
                last_login=device.last_login,
                is_active=device.is_active
            )
        return None
    except Exception as e:
        logger.error(f"Error getting device: {e}")
        raise

async def update_device(session: AsyncSession, device_id: str, device: DeviceSchema) -> DeviceSchema:
    try:
        query = (
            update(Device)
            .where(Device.device_id == device_id)
            .values(
                device_name=device.device_name,
                os_name=device.os_name,
                os_version=device.os_version,
                browser_name=device.browser_name,
                browser_version=device.browser_version,
                last_login=device.last_login,
                is_active=device.is_active
            )
        )
        await session.execute(query)
        await session.commit()
        return device
    except Exception as e:
        logger.error(f"Error updating device: {e}")
        await session.rollback()
        raise

async def delete_device(session: AsyncSession, device_id: str) -> bool:
    try:
        query = delete(Device).where(Device.device_id == device_id)
        result = await session.execute(query)
        await session.commit()
        return result.rowcount > 0
    except Exception as e:
        logger.error(f"Error deleting device: {e}")
        await session.rollback()
        raise
