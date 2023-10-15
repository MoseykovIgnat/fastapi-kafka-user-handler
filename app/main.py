from fastapi import FastAPI
from loguru import logger

from app.core.settings import app_settings
from app.routers.api import main_router

app = FastAPI(
    title="FastAPI and Kafka Users Handler",
    version="0.1.0",
)
app.include_router(main_router)


@app.get("/")
def read_root() -> str:
    return "FastAPI and Kafka User Handler."


@app.on_event("startup")
async def startup():
    logger.success(
        f"User handler microservice was successfully started. Environment: {app_settings.ENVIRONMENT}",
    )


@app.on_event("shutdown")
async def shutdown():
    logger.success(
        f"User handler microservice was successfully  stopped. Environment: {app_settings.ENVIRONMENT}",
    )
