from sqlalchemy.orm import Session

from typing import List

from db import models, schemas


def create_menu_item(db: Session, store_id: int, item_name: str, item_description: str, price: float) -> schemas.Item:
    db_item = models.MenuItem(name=item_name, description=item_description, price=price, store_id=store_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_items_by_store_id(db: Session, store_id: int) -> List[schemas.Item]:
    menu_items = db.query(models.MenuItem).filter_by(store_id=store_id)
    return [x for x in menu_items]
