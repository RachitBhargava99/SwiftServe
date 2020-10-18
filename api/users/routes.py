from fastapi import APIRouter, Depends
from etc.usrmng import fastapi_users

from db import schemas

router = APIRouter()


@router.get('', response_model=schemas.User)
def get_user_details(user: schemas.User = Depends(fastapi_users.get_current_user)):
    return user
