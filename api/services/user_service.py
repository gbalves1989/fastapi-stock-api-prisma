from fastapi import status, UploadFile
from prisma.models import Category

from api.dtos.requests.user.create_request_dto import UserCreateRequestDTO
from api.dtos.requests.user.update_request_dto import UserUpdateRequestDTO
from api.dtos.requests.user.login_request_dto import UserLoginRequestDTO
from api.dtos.responses.user.user_response_dto import (
    UserResponseDTO,
    UserWithPassResponseDTO
)
from api.repositories.user_repository import (
    signup_repository,
    find_by_email,
    update_repository,
    upload_repository
)
from api.exception.http_exception import exception_error
from api.utils.storage import (
    verify_ext_file,
    generate_hash_filename,
    upload_file,
    delete_file
)

from core.authentication.security import generate_hash_password, verify_password


async def signup_service(userCreateRequestDTO: UserCreateRequestDTO) -> UserResponseDTO:
    if userCreateRequestDTO.password != userCreateRequestDTO.confirm_password:
        raise exception_error(
            "Passwords is not equal",
            status.HTTP_400_BAD_REQUEST
        )

    email_exists: UserResponseDTO | None = await find_by_email(userCreateRequestDTO.email)

    if email_exists != None:
        raise exception_error(
            "E-mail already exists",
            status.HTTP_409_CONFLICT
        )

    hash: str = generate_hash_password(userCreateRequestDTO.password)

    user: UserResponseDTO = await signup_repository(
        userCreateRequestDTO,
        hash
    )

    return user


async def signin_service(userLoginRequestDTO: UserLoginRequestDTO) -> UserResponseDTO:
    user: UserWithPassResponseDTO | None = await find_by_email(userLoginRequestDTO.email)

    if user == None:
        raise exception_error(
            "Credencials invalid",
            status.HTTP_400_BAD_REQUEST
        )

    if not verify_password(userLoginRequestDTO.password, user.password):
        raise exception_error(
            "Credencials invalid",
            status.HTTP_400_BAD_REQUEST
        )

    return UserResponseDTO(
        id=user.id,
        name=user.name,
        email=user.email,
        avatar=user.avatar
    )


async def update_service(
    user_id: str,
    userUpdateRequestDTO: UserUpdateRequestDTO
) -> UserResponseDTO:
    if userUpdateRequestDTO.password != userUpdateRequestDTO.confirm_password:
        raise exception_error(
            "Passwords is not equal",
            status.HTTP_400_BAD_REQUEST
        )

    hash: str = generate_hash_password(userUpdateRequestDTO.password)

    user: UserResponseDTO = await update_repository(user_id, userUpdateRequestDTO, hash)
    return user


async def upload_service(user_logged: UserResponseDTO, avatar: UploadFile) -> UserResponseDTO:
    avatar_verify: bool = verify_ext_file(avatar)

    if avatar_verify == False:
        raise exception_error(
            "Type file invalid. Only select (.jpg, .jpeg, .png)",
            status.HTTP_406_NOT_ACCEPTABLE
        )

    avatar_hash_name: str = generate_hash_filename(avatar)

    if user_logged.avatar != "":
        delete_file(user_logged.avatar, "users")

    await upload_file(avatar_hash_name, "users", avatar)
    user: UserResponseDTO = await upload_repository(user_logged.id, avatar_hash_name)

    return user
