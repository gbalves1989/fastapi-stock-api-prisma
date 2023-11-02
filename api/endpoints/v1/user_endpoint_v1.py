from fastapi import APIRouter, status, Depends, UploadFile, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse, FileResponse

from slowapi import Limiter
from slowapi.util import get_remote_address

from api.dtos.requests.user.create_request_dto import UserCreateRequestDTO
from api.dtos.requests.user.update_request_dto import UserUpdateRequestDTO
from api.dtos.requests.user.login_request_dto import UserLoginRequestDTO
from api.dtos.responses.user.user_response_dto import UserResponseDTO, TokenResponseDTO
from api.services.user_service import (
    signup_service,
    signin_service,
    update_service,
    upload_service
)
from api.dtos.responses.exception_response_dto import (
    ExceptionResponseDTO,
    ExceptionRateLimitResponseDTO
)

from core.authentication.auth import create_token_access
from core.authentication.deps import get_current_user
from core.config import REQUEST_PER_MINUTES_AUTH, REQUEST_PER_MINUTES, UPLOAD_DIR

user_router_v1 = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@user_router_v1.post(
    "/signup",
    summary="Create a new user",
    description="Return a new user created with success",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponseDTO,
    responses={
        400: {"model": ExceptionResponseDTO},
        409: {"model": ExceptionResponseDTO},
        429: {"model": ExceptionRateLimitResponseDTO}
    }
)
@limiter.limit(str(REQUEST_PER_MINUTES) + "/minute")
async def signup(
    request: Request,
    userCreateRequestDTO: UserCreateRequestDTO
) -> UserResponseDTO:
    return await signup_service(userCreateRequestDTO)


@user_router_v1.post(
    "/signin",
    summary="Create token access",
    description="Return a token access with success",
    status_code=status.HTTP_200_OK,
    response_model=TokenResponseDTO,
    responses={
        400: {"model": ExceptionResponseDTO},
        429: {"model": ExceptionRateLimitResponseDTO}
    }
)
@limiter.limit(str(REQUEST_PER_MINUTES_AUTH) + "/minute")
async def signin(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends()
) -> TokenResponseDTO:
    userLoginRequestDTO: UserLoginRequestDTO = UserLoginRequestDTO(
        email=form_data.username,
        password=form_data.password
    )

    user: UserResponseDTO = await signin_service(userLoginRequestDTO)

    return JSONResponse(
        content={
            "access_token": create_token_access(sub=user.id),
            "token_type": "bearer"
        },
        status_code=status.HTTP_200_OK
    )


@user_router_v1.get(
    "/me",
    summary="Details to user logged",
    description="Return details to user logged",
    status_code=status.HTTP_200_OK,
    response_model=UserResponseDTO,
    responses={
        400: {"model": ExceptionResponseDTO},
        401: {"model": ExceptionResponseDTO},
        429: {"model": ExceptionRateLimitResponseDTO}
    }
)
@limiter.limit(str(REQUEST_PER_MINUTES) + "/minute")
async def me(
    request: Request,
    user_logged: UserResponseDTO = Depends(get_current_user)
) -> UserResponseDTO:
    return user_logged


@user_router_v1.get(
    "/file",
    summary="Avatar to user logged",
    description="Return avatar to user logged",
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ExceptionResponseDTO},
        401: {"model": ExceptionResponseDTO},
        429: {"model": ExceptionRateLimitResponseDTO}
    }
)
@limiter.limit(str(REQUEST_PER_MINUTES) + "/minute")
async def file(
    request: Request,
    user_logged: UserResponseDTO = Depends(get_current_user)
):
    return FileResponse(
        path=f"{UPLOAD_DIR}/users/{user_logged.avatar}",
        filename=user_logged.avatar
    )


@user_router_v1.put(
    "/",
    summary="Update some user logged",
    description="Return some user logged updated",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=UserResponseDTO,
    responses={
        400: {"model": ExceptionResponseDTO},
        401: {"model": ExceptionResponseDTO},
        429: {"model": ExceptionRateLimitResponseDTO}
    }
)
@limiter.limit(str(REQUEST_PER_MINUTES) + "/minute")
async def update(
    request: Request,
    userUpdateRequestDTO: UserUpdateRequestDTO,
    user_logged: UserResponseDTO = Depends(get_current_user)
) -> UserResponseDTO:
    return await update_service(user_logged.id, userUpdateRequestDTO)


@user_router_v1.patch(
    "/",
    summary="Upload avatar to user logged",
    description="Return some user logged to avatar uploaded with success",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=UserResponseDTO,
    responses={
        401: {"model": ExceptionResponseDTO},
        406: {"model": ExceptionResponseDTO},
        429: {"model": ExceptionRateLimitResponseDTO}
    }
)
@limiter.limit(str(REQUEST_PER_MINUTES) + "/minute")
async def upload(
    request: Request,
    avatar: UploadFile,
    user_logged: UserResponseDTO = Depends(get_current_user)
) -> UserResponseDTO:
    return await upload_service(user_logged, avatar)
