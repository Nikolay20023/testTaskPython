from typing import Annotated
from datetime import timedelta
from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError
from loguru import logger

from core.config import app_setting
from schemas.users import Token, TokenData, User, UserCreate, UserInfo
from service.users import user_crud
from db.db import get_session
from utils.users import (
    create_access_token,
    verify_password,
    get_password_hash,
    credentials_exception
)


router = APIRouter()

oath_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/signin")


async def get_current_user(
    token: Annotated[str, Depends(oath_scheme)],
    db: AsyncSession = Depends(get_session)
):
    try:
        payload = jwt.decode(
            token, app_setting.secret_key, app_setting.algorithm
        )
        username = payload.get("sub")
        if username is None:
            credentials_exception("Имя пользователя не может быть пустой строкой")
        token_data = TokenData(username=username)
    except JWTError:
        credentials_exception()
    
    user = await user_crud.get(db=db, username=token_data.username)
    
    if user is None:
        credentials_exception("Такой пользовательне найден")
    return user


async def authenticate_user(db, username, password):
    user = await user_crud.get(db, username=username)
    if not user :
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


@router.post(
    '/signup',
    status_code=status.HTTP_201_CREATED,
    response_model=UserCreate
)
async def signup(
    user: UserCreate,
    db: AsyncSession = Depends(get_session)
):
    password = user.hashed_password
    user.hashed_password = get_password_hash(password=password)
    try:
        new_user = await user_crud.create(db=db, obj_in=user)
    except Exception as e:
        logger.error(e)
    logger.info(new_user.__dict__)
    return UserCreate(**new_user.__dict__)


@router.post('/signin')
async def signin(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_session)
):
    user = await authenticate_user(
        db=db, username=form_data.username, password=form_data.password
    )
    if not user:
        credentials_exception("Неверный username или пароль")
    access_token_expires = timedelta(
        minutes=app_setting.access_token_expire_minutes
    )
    access_token = create_access_token(
        data={"sub": user.username}, expire_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="Bearer")


@router.get("/users/me/")
async def read_own_users(user: Annotated[UserInfo, Depends(get_current_user)]):
    return user