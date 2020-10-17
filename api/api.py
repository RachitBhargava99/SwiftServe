from fastapi import APIRouter

from api.groups.routes import router as group_router

api_router = APIRouter()

api_router.include_router(router=group_router, prefix='/group')
