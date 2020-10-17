from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from db import schemas
from db.db import get_db
from .controllers import create_store, get_store_details
from api.orders.controllers import create_order_with_items, get_all_orders_by_store_id
from api.items.controllers import get_items_by_store_id
from db.schemas import User
from etc.usrmng import fastapi_users

router = APIRouter()


@router.put('', response_model=schemas.Store)
def create_store(store: schemas.StoreCreate, db: Session = Depends(get_db), user: User = Depends(fastapi_users.get_current_user)):
    if not user.is_owner:
        raise HTTPException(403, detail="The user is not an owner")
    return JSONResponse(status_code=201, content=create_store(db, str(user.id), store.name))


@router.post('/{store_id}/order')
def create_store_order(store_id: int, order_items: schemas.OrderItemCreateList, db: Session = Depends(get_db), user: User = Depends(fastapi_users.get_current_user)):
    order_id, order = create_order_with_items(db, str(user.id), store_id, order_items.order_items)
    return JSONResponse(status_code=201, content={"order_id": order_id, "order_items": order})


@router.get('/{store_id}/order', response_model=schemas.OrderWithItemsList)
def get_store_orders(store_id: int, db: Session = Depends(get_db), user: User = Depends(fastapi_users.get_current_user)):
    if get_store_details(db, store_id).owner != user.id:
        raise HTTPException(403, detail="The user is not an owner of the selected store")
    return {"order": get_all_orders_by_store_id(db, store_id)}


@router.get('/{store_id}/item', response_model=schemas.ItemList)
def get_store_items(store_id: int, db: Session = Depends(get_db)):
    return {"items": get_items_by_store_id(db, store_id)}
