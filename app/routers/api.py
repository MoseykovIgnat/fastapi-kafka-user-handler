from fastapi import APIRouter
from app.endpoints.users import router as user_router
from app.endpoints.kafka_checker import router as kafka_checker_router
from app.endpoints.health import router as health_router

main_router = APIRouter()

main_router.include_router(health_router)
main_router.include_router(user_router)
main_router.include_router(kafka_checker_router)
