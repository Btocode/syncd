from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.auth import router as auth_router
from app.api.v1.device import router as device_router
from app.core.config import settings
from fastapi.responses import Response

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(device_router, prefix=settings.API_V1_STR)

# Health check endpoint
@app.get("/api/v1/health")
async def health_check_get():
    return Response(status_code=200)

@app.head("/api/v1/health")
async def health_check_head():
    return Response(status_code=200)

# Root endpoint
@app.get("/")
def read_root():
    """Root endpoint for the API.

    Returns:
        str: A welcome message.

    """
    return "Hello from SyncD API"
