from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from db import schemas
from db.db import get_db
from .controllers import create_store, get_store_details
from api.orders.controllers import create_order_with_items, get_all_orders_by_store_id
from api.items.controllers import get_items_by_store_id
from api.tables.controllers import get_tables_by_store_id, get_available_tables, delete_all_tables_by_store_id
from db.schemas import User
from etc.usrmng import fastapi_users

router = APIRouter()


@router.put('', response_model=schemas.Store, status_code=201)
def create_store_route(store: schemas.StoreCreate, db: Session = Depends(get_db), user: User = Depends(fastapi_users.get_current_user)):
    if not user.is_owner:
        raise HTTPException(403, detail="The user is not an owner")
    return create_store(db, str(user.id), store.name)


@router.post('/{store_id}/order', status_code=201)
def create_store_order(store_id: int, order_items: schemas.OrderItemCreateList, db: Session = Depends(get_db), user: User = Depends(fastapi_users.get_current_user)):
    order_id, order = create_order_with_items(db, str(user.id), store_id, order_items.order_items)
    return {"order_id": order_id, "order_items": order}


@router.get('/{store_id}/order', response_model=schemas.OrderWithItemsList)
def get_store_orders(store_id: int, db: Session = Depends(get_db), user: User = Depends(fastapi_users.get_current_user)):
    if get_store_details(db, store_id).owner != str(user.id):
        raise HTTPException(403, detail="The user is not an owner of the selected store")
    return {"orders": get_all_orders_by_store_id(db, store_id)}


@router.get('/{store_id}/item', response_model=schemas.ItemList)
def get_store_items(store_id: int, db: Session = Depends(get_db)):
    return {"items": get_items_by_store_id(db, store_id)}


@router.get('/{store_id}/table', response_model=schemas.TableList)
def get_all_tables(store_id: int, db: Session = Depends(get_db), user: User = Depends(fastapi_users.get_current_user)):
    if get_store_details(db, store_id).owner != str(user.id):
        raise HTTPException(403, detail="The user is not an owner of the selected store")
    return {"tables": get_tables_by_store_id(db, store_id)}


@router.delete('/{store_id}/table', response_model=schemas.TableList)
def delete_all_tables(store_id: int, db: Session = Depends(get_db), user: User = Depends(fastapi_users.get_current_user)):
    if get_store_details(db, store_id).owner != str(user.id):
        raise HTTPException(403, detail="The user is not an owner of the selected store")
    delete_all_tables_by_store_id(db, store_id)
    return {"detail": "Tables deleted successfully"}


@router.post('/{store_id}/table/available', response_model=schemas.TableList)
def get_available_tables_route(store_id: int, reservation: schemas.ReservationCreate, db: Session = Depends(get_db)):
    return {"tables": get_available_tables(db, store_id, reservation.start_time, reservation.end_time)}
