from typing import List
from fastapi import status
from prisma.models import Category

from api.dtos.requests.category.create_request_dto import CategoryCreateRequestDTO
from api.dtos.requests.category.update_request_dto import CategoryUpdateRequestDTO
from api.dtos.responses.category.category_response_dto import (
    CategoryResponseDTO,
    CategoryDetailResponseDTO
)
from api.repositories.category_repository import (
    store_repository,
    find_by_name_repository,
    show_repository,
    index_repository,
    update_repository,
    destroy_repository
)
from api.exception.http_exception import exception_error


async def store_service(categoryCreateRequestDTO: CategoryCreateRequestDTO) -> CategoryResponseDTO:
    category_name_exists: CategoryResponseDTO | None = await find_by_name_repository(
        categoryCreateRequestDTO.name
    )

    if category_name_exists != None:
        raise exception_error(
            "Category name already exists",
            status.HTTP_409_CONFLICT
        )

    category: CategoryResponseDTO = await store_repository(categoryCreateRequestDTO)
    return category


async def show_service(category_id: str) -> CategoryDetailResponseDTO:
    category: CategoryDetailResponseDTO | None = await show_repository(category_id)

    if category == None:
        raise exception_error(
            "Category not found",
            status.HTTP_404_NOT_FOUND
        )

    return category


async def index_service() -> List[CategoryResponseDTO]:
    categories: List[CategoryResponseDTO] = await index_repository()
    return categories


async def update_service(
    category_id: str,
    categoryUpdateRequestDTO: CategoryUpdateRequestDTO
) -> CategoryDetailResponseDTO:
    category_exists: CategoryDetailResponseDTO | None = await show_repository(category_id)

    if category_exists == None:
        raise exception_error(
            "Category not found",
            status.HTTP_404_NOT_FOUND
        )

    category_name_exists: CategoryResponseDTO | None = await find_by_name_repository(
        categoryUpdateRequestDTO.name
    )

    if category_name_exists != None:
        raise exception_error(
            "Category name already exists",
            status.HTTP_409_CONFLICT
        )

    category: CategoryDetailResponseDTO = await update_repository(
        category_id,
        categoryUpdateRequestDTO
    )

    return category


async def destroy_service(category_id: str) -> None:
    category: CategoryDetailResponseDTO | None = await show_repository(category_id)

    if category == None:
        raise exception_error(
            "Category not found",
            status.HTTP_404_NOT_FOUND
        )

    if category.products != []:
        raise exception_error(
            "Category have relationship with products registered",
            status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    await destroy_repository(category_id)
