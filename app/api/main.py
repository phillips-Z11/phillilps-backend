from fastapi import APIRouter

from app.api.routes import email

api_router = APIRouter()
api_router.include_router(email.router)
