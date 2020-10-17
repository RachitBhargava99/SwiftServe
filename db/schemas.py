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
# Group Models start here
# ===================================
class User(user_models.BaseUser):
    is_owner: Optional[bool] = False


class UserCreate(user_models.BaseUserCreate):
    pass


class UserUpdate(User, user_models.BaseUserUpdate):
    pass


class UserDB(User, user_models.BaseUserDB):
    pass
