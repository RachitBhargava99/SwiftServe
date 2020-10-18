from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import schemas
from db.db import get_db
from .controllers import update_order_status, get_order_by_id, get_order_items_by_order_id
from api.stores.controllers import get_store_details
from db.schemas import User
from etc.usrmng import fastapi_users

router = APIRouter()


@router.patch('/{order_id}/start', response_model=schemas.Order)
def start_making_order(order_id: int, db: Session = Depends(get_db), user: User = Depends(fastapi_users.get_current_user)):
    if get_store_details(db, get_order_by_id(db, order_id).store_id).owner != str(user.id):
        raise HTTPException(403, detail="The user is not an owner of the selected store")
    return update_order_status(db, order_id, 1)


@router.patch('/{order_id}/complete', response_model=schemas.Order)
def complete_making_order(order_id: int, db: Session = Depends(get_db), user: User = Depends(fastapi_users.get_current_user)):
    if get_store_details(db, get_order_by_id(db, order_id).store_id).owner != str(user.id):
        raise HTTPException(403, detail="The user is not an owner of the selected store")
    return update_order_status(db, order_id, 2)


@router.get('/{order_id}', response_model=schemas.OrderWithItems)
def get_order_route(order_id: int, db: Session = Depends(get_db), user: User = Depends(fastapi_users.get_current_user)):
    order = get_order_by_id(db, order_id)
    if get_store_details(db, order.store_id).owner != str(user.id) and order.buyer != str(user.id):
        raise HTTPException(403, detail="The user is not related to the selected order")
    order.order_items = get_order_items_by_order_id(db, order_id)
    return order
