from pydantic import BaseModel
from fastapi_users import models as user_models

from datetime import datetime
from typing import List, Optional


# ===================================
# Group Models start here
# ===================================
class GroupBase(BaseModel):
    name: str


class Group(GroupBase):
    id: int
    creation_time: datetime
    is_active: bool
    spotify_token: Optional[str]

    class Config:
        orm_mode = True


class GroupCreate(GroupBase):
    class Config:
        orm_mode = True


class GroupList(BaseModel):
    groups: List[Group]


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
    status: int = 0     # 0 for incomplete, 1 for making, 2 for complete

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
