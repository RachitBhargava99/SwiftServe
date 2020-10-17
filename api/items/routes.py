from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import schemas
from db.db import get_db
from .controllers import create_menu_item
from db.schemas import User
from etc.usrmng import fastapi_users

router = APIRouter()


@router.put('', response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db), user: User = Depends(fastapi_users.get_current_user)):
    print(user)
    if not user.is_owner:
        raise HTTPException(403, detail="The user is not an owner")
    db_item = create_menu_item(db, item.store_id, item.name, item.description, item.price)
    return db_item
