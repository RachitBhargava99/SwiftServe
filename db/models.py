from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase

from .db import Base


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(127), unique=True)
    creation_time = Column(DateTime)
    is_active = Column(Boolean, default=True)
    spotify_token = Column(String(255))


class UserTable(Base, SQLAlchemyBaseUserTable):
    is_owner = Column(Boolean, default=False)
    ncr_account_num = Column(String(31))


class MenuItem(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(127), unique=True)
    description = Column(String(255), unique=False)
    price = Column(Float)
    store_id = Column(Integer, ForeignKey('stores.id'))


class Store(Base):
    __tablename__ = 'stores'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(127), unique=True)
    owner = Column(String, ForeignKey('user.id'))


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey('user.id'))
    buyer = Column(String, ForeignKey('user.id'))


class OrderItem(Base):
    __tablename__ = 'orderitems'

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey('items.id'))
    quantity = Column(Integer)
    order_id = Column(Integer, ForeignKey('orders.id'))
