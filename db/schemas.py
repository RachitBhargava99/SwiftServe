from pydantic import BaseModel
from fastapi_users import models as user_models

from datetime import datetime
from typing import List, Optional


# ===================================
# User Models start here
# ===================================
class User(user_models.BaseUser):
    ncr_account_num: Optional[str] = ""
    is_owner: Optional[bool] = False


class UserCreate(user_models.BaseUserCreate):
    pass


class UserUpdate(User, user_models.BaseUserUpdate):
    pass


class UserDB(User, user_models.BaseUserDB):
    pass


# ===================================
# Item Models start here
# ===================================
class ItemBase(BaseModel):
    name: str
    description: Optional[str]
    price: float
    store_id: int


class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True


class ItemCreate(ItemBase):
    class Config:
        orm_mode = True


class ItemList(BaseModel):
    items: List[Item]


# ===================================
# Store Models start here
# ===================================
class StoreBase(BaseModel):
    name: str


class Store(StoreBase):
    id: int
    owner: str

    class Config:
        orm_mode = True


class StoreCreate(StoreBase):
    class Config:
        orm_mode = True


class StoreList(BaseModel):
    stores: List[Store]


# ===================================
# Order Item Models start here
# ===================================
class OrderItemBase(BaseModel):
    item_id: int
    quantity: int


class OrderItem(OrderItemBase):
    id: Optional[int]
    order_id: Optional[int]
    name: Optional[str]

    class Config:
        orm_mode = True


class OrderItemCreate(OrderItemBase):
    class Config:
        orm_mode = True


class OrderItemCreateList(BaseModel):
    order_items: List[OrderItemCreate]


class OrderItemList(BaseModel):
    order_items: List[OrderItem]


# ===================================
# Order Models start here
# ===================================
class OrderBase(BaseModel):
    store_id: int
    buyer: str


class Order(OrderBase):
    id: int
    status: int     # 0 for incomplete, 1 for making, 2 for complete

    class Config:
        orm_mode = True


class OrderCreate(OrderBase):
    class Config:
        orm_mode = True


class OrderList(BaseModel):
    orders: List[Order]


class OrderWithItems(Order, OrderItemList):
    class Config:
        orm_mode = True


class OrderWithItemsList(BaseModel):
    orders: List[OrderWithItems]


# ===================================
# Table Models start here
# ===================================
class TableBase(BaseModel):
    store_id: int
    internal_id: str
    x_coords: int
    y_coords: int
    width: int
    height: int
    cap: int


class Table(TableBase):
    id: int

    class Config:
        orm_mode = True


class TableCreate(TableBase):
    class Config:
        orm_mode = True


class TableList(BaseModel):
    tables: List[Table]


# ===================================
# Reservation Models start here
# ===================================
class ReservationBase(BaseModel):
    start_time: datetime
    end_time: datetime


class Reservation(ReservationBase):
    id: int
    table_id: int
    customer_id: str
    order_id: int

    class Config:
        orm_mode = True


class ReservationCreate(ReservationBase):
    class Config:
        orm_mode = True


class ReservationList(BaseModel):
    tables: List[Reservation]


class ReservationWithOrderItems(ReservationCreate, OrderItemCreateList):
    class Config:
        orm_mode = True
