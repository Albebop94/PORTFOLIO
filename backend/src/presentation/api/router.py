from fastapi import APIRouter

from src.presentation.api.routes import users

api_router = APIRouter()
api_router.include_router(users.router)
