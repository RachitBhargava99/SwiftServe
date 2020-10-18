from sqlalchemy.orm import Session

from typing import List
from api.tables.controllers import get_tables_by_store_id

from db import models, schemas


def create_store(db: Session, owner: str, name: str) -> schemas.Store:
    db_item = models.Store(name=name, owner=owner)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_all_stores(db: Session) -> List[schemas.Store]:
    all_stores = db.query(models.Store).all()
    return [x for x in all_stores]


def get_store_details(db: Session, store_id: int) -> schemas.Store:
    return db.query(models.Store).filter_by(id=store_id).first()


def get_reservations_by_table_id(db: Session, table_id: int) -> List[schemas.Reservation]:
    return [x for x in db.query(models.Reservation).filter_by(table_id=table_id)]


def get_all_reservations_by_store_id(db: Session, store_id: int) -> List[schemas.Reservation]:
    all_reservations = []
    all_tables = get_tables_by_store_id(db, store_id)
    for curr_table in all_tables:
        all_reservations += get_reservations_by_table_id(db, curr_table.id)
    return all_reservations
