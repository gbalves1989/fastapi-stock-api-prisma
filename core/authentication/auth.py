from fastapi.security import OAuth2PasswordBearer
from core.config import (
    API_VERSION,
    JWT_SECRET,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from datetime import datetime, timedelta
from pytz import timezone
from jose import jwt

oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f"{API_VERSION}/users/signin"
)


def _create_token(type_token: str, time_life: timedelta, sub: str) -> str:
    payload = {}

    sp = timezone("America/Sao_Paulo")
    expire_in = datetime.now(tz=sp) + time_life

    payload["type"] = type_token
    payload["exp"] = expire_in
    payload["iat"] = datetime.now(tz=sp)
    payload["sub"] = str(sub)

    return jwt.encode(payload, key=JWT_SECRET, algorithm=ALGORITHM)


def create_token_access(sub: str) -> str:
    return _create_token(
        type_token="access_token",
        time_life=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub
    )
