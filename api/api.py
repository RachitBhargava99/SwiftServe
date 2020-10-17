from fastapi import APIRouter

from api.groups.routes import router as group_router
from api.items.routes import router as item_router
from api.orders.routes import router as order_router
from api.stores.routes import router as store_router

api_router = APIRouter()

api_router.include_router(router=group_router, prefix='/group')
api_router.include_router(router=item_router, prefix='/item')
api_router.include_router(router=order_router, prefix='/order')
api_router.include_router(router=store_router, prefix='/store')
