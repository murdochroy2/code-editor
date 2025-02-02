from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from app.core.config import settings
from app.api import auth, collaboration, code_files

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="""
    Real-Time Collaborative Code Editor API
    
    Features:
    * 👥 User authentication and management
    * 📝 Real-time collaborative code editing
    * 🤖 AI-assisted debugging
    * 📁 Code file management
    """,
    version="1.0.0",
)

# Set up CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(
    collaboration.router,
    prefix=f"{settings.API_V1_STR}/collaboration",
    tags=["collaboration"]
)
app.include_router(
    code_files.router,
    prefix=f"{settings.API_V1_STR}/files",
    tags=["files"]
)
