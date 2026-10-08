from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes.files import router as files_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.db.init_db import init_db


setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan
)


app.include_router(files_router)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version
    }