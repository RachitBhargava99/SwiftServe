from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import schemas
from db.db import get_db
from .controllers import get_group_by_name

router = APIRouter()


@router.get('/', response_model=schemas.Group)
def create_group_route(group: schemas.GroupCreate, db: Session = Depends(get_db)):
    db_group = get_group_by_name(db, group_name=group.name)
    if db_group:
        raise HTTPException(status_code=422, detail="Group name already exists")
    return "User Found!"
