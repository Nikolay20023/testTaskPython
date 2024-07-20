from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from core.config import app_setting
from jose import jwt


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def credentials_exception(message="Could not validate credentials"):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"{message}",
        headers={"WWW-Authenticate": "Bearer"}
    )


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expire_delta: timedelta | None = None):
    to_encode = data.copy()
    if expire_delta:
        expire = datetime.now(timezone.utc) + expire_delta
        
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(
        to_encode, app_setting.secret_key, app_setting.algorithm
    )
    return encode_jwt