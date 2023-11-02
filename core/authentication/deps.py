from fastapi import Depends
from jose import jwt, JWTError

from api.dtos.responses.user.user_response_dto import UserResponseDTO
from api.exception.http_exception import exception_error_credential
from api.repositories.user_repository import find_by_id

from core.authentication.auth import oauth2_schema
from core.config import JWT_SECRET, ALGORITHM


async def get_current_user(
    token: str = Depends(oauth2_schema)
) -> UserResponseDTO:
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[ALGORITHM],
            options={"verify_aud": False}
        )

        username: str = payload.get("sub")

        if username is None:
            raise exception_error_credential()

        user: UserResponseDTO | None = await find_by_id(username)

        if user == None:
            raise exception_error_credential()

        return user
    except JWTError:
        raise exception_error_credential()
