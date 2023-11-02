from typing import List
from core.prisma_connection import prisma_connection

from prisma import Prisma
from prisma.models import User

from api.dtos.requests.user.create_request_dto import UserCreateRequestDTO
from api.dtos.requests.user.update_request_dto import UserUpdateRequestDTO
from api.dtos.responses.user.user_response_dto import UserResponseDTO, UserWithPassResponseDTO

prisma_db: Prisma = Prisma()


async def signup_repository(
    userCreateRequestDTO: UserCreateRequestDTO,
    hash: str
) -> UserResponseDTO:
    await prisma_db.connect()
    user: User = await prisma_db.user.create({
        "name": userCreateRequestDTO.name,
        "email": userCreateRequestDTO.email,
        "password": hash
    })
    await prisma_db.disconnect()

    return UserResponseDTO(
        id=user.id,
        name=user.name,
        email=user.email,
        avatar=user.avatar
    )


async def find_by_email(email: str) -> UserWithPassResponseDTO | None:
    await prisma_db.connect()
    user: User = await prisma_db.user.find_unique({"email": email})
    await prisma_db.disconnect()

    if user != None:
        return UserWithPassResponseDTO(
            id=user.id,
            name=user.name,
            email=user.email,
            password=user.password,
            avatar=user.avatar
        )

    return None


async def find_by_id(user_id: str) -> UserResponseDTO | None:
    await prisma_db.connect()
    user: User = await prisma_db.user.find_unique({"id": user_id})
    await prisma_db.disconnect()

    if user != None:
        return UserResponseDTO(
            id=user.id,
            name=user.name,
            email=user.email,
            avatar=user.avatar
        )

    return None


async def update_repository(
    user_id: str,
    userUpdateRequestDTO: UserUpdateRequestDTO,
    hash: str
) -> UserResponseDTO:
    await prisma_db.connect()
    user: User = await prisma_db.user.update(
        data={
            "name": userUpdateRequestDTO.name,
            "password": hash
        },
        where={"id": user_id}
    )
    await prisma_db.disconnect()

    return UserResponseDTO(
        id=user.id,
        name=user.name,
        email=user.email,
        avatar=user.avatar
    )


async def upload_repository(user_id: str, avatar: str) -> UserResponseDTO:
    await prisma_db.connect()
    user: User = await prisma_db.user.update(
        data={"avatar": avatar},
        where={"id": user_id}
    )
    await prisma_db.disconnect()

    return UserResponseDTO(
        id=user.id,
        name=user.name,
        email=user.email,
        avatar=user.avatar
    )
