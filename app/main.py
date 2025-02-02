from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import auth, collaboration, code_files

app = FastAPI(title=settings.PROJECT_NAME)

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