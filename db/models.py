from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey
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
