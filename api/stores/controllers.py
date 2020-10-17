from sqlalchemy.orm import Session

from typing import List

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
