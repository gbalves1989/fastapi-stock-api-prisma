from typing import List
from core.prisma_connection import prisma_connection

from prisma import Prisma
from prisma.models import Product

from api.dtos.requests.product.create_request_dto import ProductCreateRequestDTO
from api.dtos.requests.product.update_request_dto import ProductUpdateRequestDTO
from api.dtos.responses.product.product_response_dto import (
    ProductResponseDTO,
    ProductNameResponseDTO
)

prisma_db: Prisma = Prisma()


async def store_repository(productCreateRequestDTO: ProductCreateRequestDTO) -> ProductResponseDTO:
    await prisma_db.connect()
    product: Product = await prisma_db.product.create(
        data={
            "name": productCreateRequestDTO.name,
            "description": productCreateRequestDTO.description,
            "categoryId": productCreateRequestDTO.category_id
        },
        include={"category": True}
    )
    await prisma_db.disconnect()

    category: object = {
        "id": product.category.id,
        "name": product.category.name
    }

    return ProductResponseDTO(
        id=product.id,
        name=product.name,
        description=product.description,
        banner=product.banner,
        category=category
    )


async def find_by_name_repository(name: str) -> ProductNameResponseDTO | None:
    await prisma_db.connect()
    product: Product = await prisma_db.product.find_unique({"name": name})
    await prisma_db.disconnect()

    if product != None:
        return ProductNameResponseDTO(
            id=product.id,
            name=product.name,
            description=product.description,
            banner=product.banner
        )

    return None


async def show_repository(product_id: str) -> ProductResponseDTO | None:
    await prisma_db.connect()
    product: Product = await prisma_db.product.find_unique(
        where={"id": product_id},
        include={"category": True}
    )
    await prisma_db.disconnect()

    if product != None:
        category: object = {
            "id": product.category.id,
            "name": product.category.name
        }

        return ProductResponseDTO(
            id=product.id,
            name=product.name,
            description=product.description,
            banner=product.banner,
            category=category
        )

    return None


async def index_repository() -> List[ProductResponseDTO]:
    await prisma_db.connect()
    products_db: List[Product] = await prisma_db.product.find_many(include={"category": True})
    await prisma_db.disconnect()

    products: List = []

    for product in products_db:
        category: object = {
            "id": product.category.id,
            "name": product.category.name
        }

        products.append({
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "banner": product.banner,
            "category": category
        })

    return products


async def update_repository(
    product_id: str,
    productUpdateRequestDTO: ProductUpdateRequestDTO
) -> ProductResponseDTO:
    await prisma_db.connect()
    product: Product = await prisma_db.product.update(
        data={
            "name": productUpdateRequestDTO.name,
            "description": productUpdateRequestDTO.description
        },
        where={"id": product_id},
        include={"category": True}
    )
    await prisma_db.disconnect()

    category: object = {
        "id": product.category.id,
        "name": product.category.name
    }

    return ProductResponseDTO(
        id=product.id,
        name=product.name,
        description=product.description,
        banner=product.banner,
        category=category
    )


async def upload_repository(product_id: str, banner: str) -> ProductResponseDTO:
    await prisma_db.connect()
    product: Product = await prisma_db.product.update(
        data={"banner": banner},
        where={"id": product_id},
        include={"category": True}
    )
    await prisma_db.disconnect()

    category: object = {
        "id": product.category.id,
        "name": product.category.name
    }

    return ProductResponseDTO(
        id=product.id,
        name=product.name,
        description=product.description,
        banner=product.banner,
        category=category
    )


async def destroy_repository(product_id: str) -> None:
    await prisma_db.connect()
    await prisma_db.product.delete({"id": product_id})
    await prisma_db.disconnect()
