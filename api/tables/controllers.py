from sqlalchemy.orm import Session

from typing import List
from datetime import datetime

from db import models, schemas


def create_table(db: Session, table: schemas.TableCreate) -> schemas.Table:
    db_item = models.Table(store_id=table.store_id, internal_id=table.internal_id, x_coords=table.x_coords,
                           y_coords=table.y_coords, width=table.width, height=table.height, cap=table.cap)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_tables_by_store_id(db: Session, store_id: int) -> List[schemas.Table]:
    return [x for x in db.query(models.Table).filter_by(store_id=store_id)]


def get_reservations_by_table_id(db: Session, table_id: int) -> List[schemas.Reservation]:
    return [x for x in db.query(models.Reservation).filter_by(table_id=table_id)]


def is_available(db: Session, table_id: int, start_time: datetime, end_time: datetime) -> bool:
    all_reservations = get_reservations_by_table_id(db, table_id)
    start_time = start_time.replace(tzinfo=None)
    end_time = end_time.replace(tzinfo=None)
    for past_reservation in all_reservations:
        if start_time <= past_reservation.start_time <= end_time \
                or start_time <= past_reservation.end_time <= end_time \
                or past_reservation.start_time <= start_time <= past_reservation.end_time:
            return False
    return True


def reserve_table(db: Session, table_id: int, customer_id: str, reservation: schemas.ReservationCreate) -> schemas.Reservation:
    db_item = models.Reservation(customer_id=customer_id, table_id=table_id,
                                 start_time=reservation.start_time, end_time=reservation.end_time)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_available_tables(db: Session, store_id: int, start_time: datetime, end_time:datetime) -> List[schemas.Table]:
    return [x for x in get_tables_by_store_id(db, store_id) if is_available(db, x.id, start_time, end_time)]


def get_table_by_id(db: Session, table_id: int) -> schemas.Table:
    return db.query(models.Table).filter_by(id=table_id).first()


def delete_table_by_id(db: Session, table_id: int) -> bool:
    db.query(models.Table).filter_by(id=table_id).delete()
    db.commit()
    return True


def delete_all_tables_by_store_id(db: Session, store_id: int) -> bool:
    db.query(models.Table).filter_by(store_id=store_id).delete()
    db.commit()
    return True
