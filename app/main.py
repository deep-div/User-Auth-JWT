from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.router import router
from app.db.session import engine
from app.db.base import Base
from shared.logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles application startup and shutdown"""
    logger.info("Starting Auth Service")
    Base.metadata.create_all(bind=engine)
    yield
    logger.info("Shutting down Auth Service")
app = FastAPI(lifespan=lifespan)

app.include_router(router)



# py -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000