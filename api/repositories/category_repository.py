from typing import List
from core.prisma_connection import prisma_connection

from prisma import Prisma
from prisma.models import Category, Product

from api.dtos.responses.category.category_response_dto import (
    CategoryResponseDTO,
    CategoryDetailResponseDTO
)
from api.dtos.requests.category.create_request_dto import CategoryCreateRequestDTO
from api.dtos.requests.category.update_request_dto import CategoryUpdateRequestDTO

prisma_db: Prisma = Prisma()


async def store_repository(categoryCreateRequestDTO: CategoryCreateRequestDTO) -> CategoryResponseDTO:
    await prisma_db.connect()
    category: Category = await prisma_db.category.create({
        "name": categoryCreateRequestDTO.name,
    })
    await prisma_db.disconnect()

    return CategoryResponseDTO(
        id=category.id,
        name=category.name
    )


async def find_by_name_repository(name: str) -> CategoryResponseDTO | None:
    await prisma_db.connect()
    category: Category = await prisma_db.category.find_unique({"name": name})
    await prisma_db.disconnect()

    if category != None:
        return CategoryResponseDTO(
            id=category.id,
            name=category.name
        )

    return None


async def show_repository(category_id: str) -> CategoryDetailResponseDTO | None:
    await prisma_db.connect()
    category: Category = await prisma_db.category.find_unique(
        where={"id": category_id},
        include={"Product": True}
    )
    await prisma_db.disconnect()

    if category != None:
        products: List = []

        for product in category.Product:
            products.append({
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "banner": product.banner
            })

        return CategoryDetailResponseDTO(
            id=category.id,
            name=category.name,
            products=products
        )

    return None


async def index_repository() -> List[CategoryResponseDTO]:
    await prisma_db.connect()
    categories: List[Category] = await prisma_db.category.find_many()
    await prisma_db.disconnect()

    return categories


async def update_repository(
    category_id: str,
    categoryUpdateRequestDTO: CategoryUpdateRequestDTO
) -> CategoryDetailResponseDTO:
    await prisma_db.connect()
    category: Category = await prisma_db.category.update(
        data={"name": categoryUpdateRequestDTO.name},
        where={"id": category_id},
        include={"Product": True}
    )
    await prisma_db.disconnect()

    products: List = []

    for product in category.Product:
        products.append({
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "banner": product.banner
        })

    return CategoryDetailResponseDTO(
        id=category.id,
        name=category.name,
        products=products
    )


async def destroy_repository(category_id: str) -> None:
    await prisma_db.connect()
    await prisma_db.category.delete({"id": category_id})
    await prisma_db.disconnect()
