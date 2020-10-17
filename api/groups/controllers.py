from sqlalchemy.orm import Session

from db import models, schemas


def get_group_by_name(db: Session, group_name: str) -> schemas.Group:
    return db.query(models.Group).filter_by(name=group_name).first()
