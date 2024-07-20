from pydantic import BaseModel
from typing import List
import uuid
from schemas.weather import WeatherCreate


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str


class UserCreate(User):
    hashed_password: str


class UserUpdate(User):
    pass


class UserInfo(User):
    weathers: List[WeatherCreate]