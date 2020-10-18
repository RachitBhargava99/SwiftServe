from sqlalchemy.orm import Session

from typing import List, Tuple

from db import models, schemas


def create_order(db: Session, buyer: str, store_id: int) -> schemas.Order:
    db_item = models.Order(store_id=store_id, buyer=buyer)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def create_order_item(db: Session, order_id: int, item_id: int, quantity: int) -> schemas.OrderItem:
    db_item = models.OrderItem(item_id=item_id, quantity=quantity, order_id=order_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def create_order_with_items(db: Session, buyer: str, store_id: int, order_items: List[schemas.OrderItemCreate]) -> Tuple[int, List[schemas.OrderItem]]:
    order = create_order(db, buyer, store_id)
    db_order_items = [create_order_item(db, order.id, curr_item.item_id, curr_item.quantity).__dict__ for curr_item in order_items]
    return order.id, db_order_items


def get_order_items_by_order_id(db: Session, order_id: int) -> List[schemas.OrderItem]:
    all_items = db.query(models.OrderItem).filter_by(order_id=order_id)
    return [x for x in all_items]


def get_all_orders_by_store_id(db: Session, store_id: int) -> List[schemas.OrderWithItems]:
    all_orders = [x for x in db.query(models.Order).filter_by(store_id=store_id)]
    for curr_order in all_orders:
        curr_order.order_items = get_order_items_by_order_id(db, curr_order.id)
    return all_orders


def get_order_by_id(db: Session, order_id: int) -> schemas.Order:
    return db.query(models.Order).filter_by(id=order_id).first()


def update_order_status(db: Session, order_id: int, new_status: int) -> schemas.Order:
    db_order = get_order_by_id(db, order_id)
    db_order.status = new_status
    db.commit()
    db.refresh(db_order)
    return db_order
