# app/api/v1/auth.py
from datetime import datetime, timedelta
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.app_logging import logger
from app.core.security import create_access_token, create_refresh_token, get_password_hash, verify_password
from app.db.database import get_session
from app.db.models import User
from app.schemas.auth import LoginSchema, SignupSchema, TokenSchema, UserInfo
from app.services.supabase import supabase

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=TokenSchema)
async def signup(
    signup_data: SignupSchema,
    session: AsyncSession = Depends(get_session)
):
    try:
        # Check if user already exists
        query = select(User).where(User.email == signup_data.email)
        result = await session.execute(query)
        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="User with this email already exists"
            )

        # Create new user
        new_user = User(
            user_id=str(uuid4()),
            email=signup_data.email,
            hashed_password=get_password_hash(signup_data.password),
            display_name=signup_data.display_name
        )

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        # Generate token
        access_token = create_access_token(data={"sub": new_user.user_id})
        refresh_token = create_refresh_token(data={"sub": new_user.user_id})

        return TokenSchema(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user_info={
                "user_id": new_user.user_id,
                "email": new_user.email,
                "display_name": new_user.display_name
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        logger.error(f"Signup error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=TokenSchema)
async def login(
    login_data: LoginSchema,
    response: Response,
    session: AsyncSession = Depends(get_session)
):
    try:
        # Find user by email
        query = select(User).where(User.email == login_data.email)
        result = await session.execute(query)
        user = result.scalar_one_or_none()

        if not user or not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=401,
                detail="Incorrect email or password"
            )

        # Generate token
        access_token = create_access_token(data={"sub": user.user_id})
        refresh_token = create_refresh_token(data={"sub": user.user_id})
        return TokenSchema(
            user_info=UserInfo(
                user_id=user.user_id,
                email=user.email,
                display_name=user.display_name
            ),
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(status_code=401, detail="Invalid credentials")


@router.get("/login/{provider}")
async def social_login(provider: str):
    """Handle social login through Supabase"""
    try:
        return await supabase.client.auth.sign_in_with_provider({
            "provider": provider
        })
    except Exception as e:
        logger.error(f"Social login error: {e}")
        raise HTTPException(status_code=400, detail=str(e))