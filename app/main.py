import asyncio

from fastapi import FastAPI
from loguru import logger

from app.core.app_settings import get_app_settings
from app.kafka_workers.consumer import kafka_consumer
from app.kafka_workers.producer import kafka_producer
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
    await kafka_producer.producer_client.start()
    asyncio.get_event_loop().create_task(kafka_consumer.consume_messages())
    logger.success(
        f"User handler microservice was successfully started. Environment: {get_app_settings().ENVIRONMENT}",
    )


@app.on_event("shutdown")
async def shutdown():
    logger.success(
        f"User handler microservice was successfully  stopped. Environment: {get_app_settings().ENVIRONMENT}",
    )
