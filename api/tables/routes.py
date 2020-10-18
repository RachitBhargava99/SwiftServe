from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import schemas
from db.db import get_db
from .controllers import create_table, is_available, reserve_table, delete_table_by_id, get_table_by_id
from api.orders.controllers import create_order_with_items
from api.stores.controllers import get_store_details
from db.schemas import User
from etc.usrmng import fastapi_users

router = APIRouter()


@router.put('', response_model=schemas.Table, status_code=201)
def create_store_route(table: schemas.TableCreate, db: Session = Depends(get_db), user: User = Depends(fastapi_users.get_current_user)):
    if not user.is_owner:
        raise HTTPException(403, detail="The user is not an owner")
    if get_store_details(db, table.store_id).owner != str(user.id):
        raise HTTPException(403, detail="The user is not an owner of the selected store")
    return create_table(db, table)


@router.delete('/{table_id}', status_code=200)
def delete_table_route(table_id: int, db: Session = Depends(get_db), user: User = Depends(fastapi_users.get_current_user)):
    if not user.is_owner:
        raise HTTPException(403, detail="The user is not an owner")
    table = get_table_by_id(db, table_id)
    if table is None:
        raise HTTPException(400, detail="Incorrect / invalid table ID provided")
    if get_store_details(db, table.store_id).owner != str(user.id):
        raise HTTPException(403, detail="The user is not an owner of the store where the table is located")
    delete_table_by_id(db, table_id)
    return {"detail": "Table deleted successfully"}


@router.put('/{table_id}/reserve', response_model=schemas.Reservation, status_code=201)
def reserve_table_route(table_id: int, reservation_with_order: schemas.ReservationWithOrderItems, db: Session = Depends(get_db), user: User = Depends(fastapi_users.get_current_user)):
    if not is_available(db, table_id, reservation_with_order.start_time, reservation_with_order.end_time):
        raise HTTPException(409, "Another reservation has a conflict with the requested time")
    order_id, _ = create_order_with_items(db, str(user.id), get_table_by_id(db, table_id).store_id, reservation_with_order.order_items)
    return reserve_table(db, table_id, str(user.id), reservation_with_order, order_id)
