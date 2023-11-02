from typing import List
from fastapi import status, UploadFile
from prisma.models import Product

from api.dtos.requests.product.create_request_dto import ProductCreateRequestDTO
from api.dtos.requests.product.update_request_dto import ProductUpdateRequestDTO
from api.dtos.responses.product.product_response_dto import (
    ProductResponseDTO,
    ProductNameResponseDTO
)
from api.dtos.responses.category.category_response_dto import CategoryDetailResponseDTO
from api.repositories.product_repository import (
    store_repository,
    find_by_name_repository,
    show_repository,
    index_repository,
    update_repository,
    upload_repository,
    destroy_repository
)
from api.repositories.category_repository import show_repository as show_repository_by_category
from api.exception.http_exception import exception_error
from api.utils.storage import (
    verify_ext_file,
    generate_hash_filename,
    upload_file,
    delete_file
)


async def store_service(productCreateRequestDTO: ProductCreateRequestDTO) -> ProductResponseDTO:
    category_exists: CategoryDetailResponseDTO | None = await show_repository_by_category(
        productCreateRequestDTO.category_id
    )

    if category_exists == None:
        raise exception_error(
            "Category not found",
            status.HTTP_404_NOT_FOUND
        )

    product_name_exists: ProductNameResponseDTO | None = await find_by_name_repository(
        productCreateRequestDTO.name
    )

    if product_name_exists != None:
        raise exception_error(
            "Product name already exists",
            status.HTTP_409_CONFLICT
        )

    product: ProductResponseDTO = await store_repository(productCreateRequestDTO)
    return product


async def show_service(category_id: str) -> ProductResponseDTO:
    product: ProductResponseDTO | None = await show_repository(category_id)

    if product == None:
        raise exception_error(
            "Category not found",
            status.HTTP_404_NOT_FOUND
        )

    return product


async def index_service() -> List[ProductResponseDTO]:
    products: List[ProductResponseDTO] = await index_repository()
    return products


async def update_service(
    product_id: str,
    productUpdateRequestDTO: ProductUpdateRequestDTO
) -> ProductResponseDTO:
    product_exists: ProductResponseDTO | None = await show_repository(product_id)

    if (product_exists == None):
        raise exception_error(
            "Product not found",
            status.HTTP_404_NOT_FOUND
        )

    product_name_exists: ProductResponseDTO | None = await find_by_name_repository(
        productUpdateRequestDTO.name
    )

    if product_name_exists != None:
        raise exception_error(
            "Product name already exists",
            status.HTTP_409_CONFLICT
        )

    product: ProductResponseDTO = await update_repository(
        product_id,
        productUpdateRequestDTO
    )

    return product


async def upload_service(product_id: str, banner: UploadFile) -> ProductResponseDTO:
    product: ProductResponseDTO | None = await show_repository(product_id)

    if (product == None):
        raise exception_error(
            "Product not found",
            status.HTTP_404_NOT_FOUND
        )

    banner_verify: bool = verify_ext_file(banner)

    if banner_verify == False:
        raise exception_error(
            "Type file invalid. Only select (.jpg, .jpeg, .png)",
            status.HTTP_406_NOT_ACCEPTABLE
        )

    banner_hash_name: str = generate_hash_filename(banner)

    if product.banner != "":
        delete_file(product.banner, "products")

    await upload_file(banner_hash_name, "products", banner)
    product: ProductResponseDTO = await upload_repository(product_id, banner_hash_name)

    return product


async def destroy_service(product_id: str) -> None:
    product_exists: ProductResponseDTO | None = await show_repository(product_id)

    if (product_exists == None):
        raise exception_error(
            "Product not found",
            status.HTTP_404_NOT_FOUND
        )

    await destroy_repository(product_id)
