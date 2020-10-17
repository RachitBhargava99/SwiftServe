from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users import FastAPIUsers
from fastapi import FastAPI, Request
from sqlalchemy.orm import Session
import requests

from db.models import UserTable
from db.schemas import User, UserCreate, UserUpdate, UserDB
from db.auth import jwt_authentication
from db.db import database, SessionLocal
from etc.ncr import get_headers

users = UserTable.__table__
user_db = SQLAlchemyUserDatabase(UserDB, database, users)

fastapi_users = FastAPIUsers(
    user_db,
    [jwt_authentication],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)


def initialize_fastapi_users(app: FastAPI):
    async def on_after_register(user: UserDB, request: Request):
        db: Session = SessionLocal()
        db_user = db.query(UserTable).filter_by(id=user.id).first()
        db_user.is_owner = user.is_owner = (await request.json()).get('is_owner', False)
        if not user.is_owner:
            response = requests.post('https://gateway-staging.ncrcloud.com/cdm/consumers', json={
                "profileUsername": user.email
            }, headers=get_headers('https://gateway-staging.ncrcloud.com/cdm/consumers', 'POST')).json()
            db_user.ncr_account_num = user.ncr_account_num = response.get('consumerAccountNumber', '')
        db.commit()
        db.refresh(db_user)
        db.close()
        print(db_user.__dict__)
        return user

    app.include_router(
        fastapi_users.get_auth_router(jwt_authentication), prefix="/auth", tags=["auth"]
    )
    app.include_router(
        fastapi_users.get_register_router(on_after_register), prefix="/auth", tags=["auth"]
    )
