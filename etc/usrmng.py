from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users import FastAPIUsers
from fastapi import FastAPI, Request
from sqlalchemy.orm import Session

from db.models import UserTable
from db.schemas import User, UserCreate, UserUpdate, UserDB
from db.auth import jwt_authentication
from db.db import database, SessionLocal

users = UserTable.__table__
user_db = SQLAlchemyUserDatabase(UserDB, database, users)


def initialize_fastapi_users(app: FastAPI):
    fastapi_users = FastAPIUsers(
        user_db,
        [jwt_authentication],
        User,
        UserCreate,
        UserUpdate,
        UserDB,
    )

    async def on_after_register(user: UserDB, request: Request):
        db: Session = SessionLocal()
        db_user = db.query(UserTable).filter_by(id=user.id)
        db_user.is_owner = user.is_owner = (await request.json()).get('is_owner', False)
        db.commit()
        db.close()

    app.include_router(
        fastapi_users.get_auth_router(jwt_authentication), prefix="/auth", tags=["auth"]
    )
    app.include_router(
        fastapi_users.get_register_router(on_after_register), prefix="/auth", tags=["auth"]
    )
