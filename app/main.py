from app.api.v1.auth import router as auth_router
from app.app_instance import create_app
from app.core.config import settings

app = create_app()

app.include_router(auth_router, prefix=settings.API_V1_STR)


# Root endpoint
@app.get("/")
def read_root():
    """Root endpoint for the API.

    Returns:
        str: A welcome message.

    """
    return "Hello from SyncD API"
