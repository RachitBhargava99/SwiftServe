from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users import FastAPIUsers
from fastapi import FastAPI, Request
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import models
from fastapi_users.authentication import Authenticator, BaseAuthentication
from fastapi_users.db import BaseUserDatabase
from fastapi_users.router.common import ErrorCode
from sqlalchemy.orm import Session
import requests

from db.models import UserTable
from db.schemas import User, UserCreate, UserUpdate, UserDB
from db.auth import jwt_authentication
from db.db import database, SessionLocal
from etc.ncr import get_headers
from db import schemas

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


def get_auth_router(
        backend: BaseAuthentication,
        user_db: BaseUserDatabase[models.BaseUserDB],
        authenticator: Authenticator,
) -> APIRouter:
    """Generate a router with login/logout routes for an authentication backend."""
    router = APIRouter()

    @router.post("/login")
    async def login(
            response: Response, credentials: OAuth2PasswordRequestForm = Depends()
    ):
        user = await user_db.authenticate(credentials)

        if user is None or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.LOGIN_BAD_CREDENTIALS,
            )

        login_response = await backend.get_login_response(user, response)
        login_response['is_owner'] = user.is_owner
        return login_response

    if backend.logout:
        @router.post("/logout")
        async def logout(
                response: Response, user=Depends(authenticator.get_current_active_user)
        ):
            return await backend.get_logout_response(user, response)

    return router


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
    app.include_router(fastapi_users.get_register_router(after_register=on_after_register), prefix="/auth", tags=["auth"])
