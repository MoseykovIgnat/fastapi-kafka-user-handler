from fastapi import APIRouter
from app.endpoints.users import router as user_router

main_router = APIRouter()

main_router.include_router(user_router)
