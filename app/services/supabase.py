from supabase import create_client, Client
from app.core.config import settings
from app.core.app_logging import logger
from app.schemas.auth import SignupSchema, LoginSchema

class SupabaseService:
    client: Client = None

    def __init__(self):
        self.client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

    async def sign_up(self, signup_data: SignupSchema):
        try:
            # Only handle authentication
            response = self.client.auth.sign_up({
                "email": signup_data.email,
                "password": signup_data.password
            })
            return response
        except Exception as e:
            logger.error(f"Sign up error: {e}")
            raise

    async def sign_in(self, login_data: LoginSchema):
        try:
            response = self.client.auth.sign_in_with_password({
                "email": login_data.email,
                "password": login_data.password
            })
            return response
        except Exception as e:
            logger.error(f"Sign in error: {e}")
            raise

    async def verify_token(self, token: str):
        try:
            response = self.client.auth.get_user(token)
            return response.user
        except Exception as e:
            logger.error(f"Token verification error: {e}")
            raise

supabase = SupabaseService()
