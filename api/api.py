from fastapi import APIRouter

from api.users.routes import router as user_router
from api.items.routes import router as item_router
from api.orders.routes import router as order_router
from api.stores.routes import router as store_router
from api.tables.routes import router as table_router
from api.webhooks.routes import router as webhook_router

api_router = APIRouter()

api_router.include_router(router=user_router, prefix='/auth')
api_router.include_router(router=item_router, prefix='/item')
api_router.include_router(router=order_router, prefix='/order')
api_router.include_router(router=store_router, prefix='/store')
api_router.include_router(router=table_router, prefix='/table')
api_router.include_router(router=webhook_router, prefix='/wh')
