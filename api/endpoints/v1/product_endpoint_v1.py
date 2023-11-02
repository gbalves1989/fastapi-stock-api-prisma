from typing import List

from fastapi import APIRouter, status, UploadFile, Depends, Request
from fastapi.responses import FileResponse

from slowapi import Limiter
from slowapi.util import get_remote_address

from api.services.product_service import (
    store_service,
    show_service,
    index_service,
    update_service,
    upload_service,
    destroy_service
)
from api.dtos.requests.product.create_request_dto import ProductCreateRequestDTO
from api.dtos.requests.product.update_request_dto import ProductUpdateRequestDTO
from api.dtos.responses.product.product_response_dto import ProductResponseDTO

from api.dtos.responses.exception_response_dto import (
    ExceptionResponseDTO,
    ExceptionRateLimitResponseDTO
)
from api.dtos.responses.user.user_response_dto import UserResponseDTO

from core.authentication.deps import get_current_user
from core.config import REQUEST_PER_MINUTES, UPLOAD_DIR

product_router_v1 = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@product_router_v1.post(
    "/",
    summary="Create a new product",
    description="Return a new product created with success",
    status_code=status.HTTP_201_CREATED,
    response_model=ProductResponseDTO,
    responses={
        401: {"model": ExceptionResponseDTO},
        404: {"model": ExceptionResponseDTO},
        409: {"model": ExceptionResponseDTO},
        429: {"model": ExceptionRateLimitResponseDTO}
    }
)
@limiter.limit(str(REQUEST_PER_MINUTES) + "/minute")
async def store(
    request: Request,
    productCreateRequestDTO: ProductCreateRequestDTO,
    user_logged: UserResponseDTO = Depends(get_current_user)
) -> ProductResponseDTO:
    return await store_service(productCreateRequestDTO)


@product_router_v1.get(
    "/{product_id}",
    summary="Get some product by id",
    description="Return some product by id",
    status_code=status.HTTP_200_OK,
    response_model=ProductResponseDTO,
    responses={
        401: {"model": ExceptionResponseDTO},
        404: {"model": ExceptionResponseDTO},
        429: {"model": ExceptionRateLimitResponseDTO}
    }
)
@limiter.limit(str(REQUEST_PER_MINUTES) + "/minute")
async def show(
    request: Request,
    product_id: str,
    user_logged: UserResponseDTO = Depends(get_current_user)
) -> ProductResponseDTO:
    return await show_service(product_id)


@product_router_v1.get(
    "/file/{product_id}",
    summary="Get banner file some product by id",
    description="Return banner file some product by id",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "content": {"image/png;image/jpg;image/jpeg": {}},
            "description": "Return an banner file.",
        },
        401: {"model": ExceptionResponseDTO},
        404: {"model": ExceptionResponseDTO},
        429: {"model": ExceptionRateLimitResponseDTO}
    }
)
@limiter.limit(str(REQUEST_PER_MINUTES) + "/minute")
async def show_file(
    request: Request,
    product_id: str,
    user_logged: UserResponseDTO = Depends(get_current_user)
):
    product: ProductResponseDTO = await show_service(product_id)
    return FileResponse(
        path=f"{UPLOAD_DIR}/products/{product.banner}",
        filename=product.banner
    )


@product_router_v1.get(
    "/",
    summary="List of products",
    description="Return some list of products",
    status_code=status.HTTP_200_OK,
    response_model=List[ProductResponseDTO],
    responses={
        401: {"model": ExceptionResponseDTO},
        429: {"model": ExceptionRateLimitResponseDTO}
    }
)
@limiter.limit(str(REQUEST_PER_MINUTES) + "/minute")
async def index(
    request: Request,
    user_logged: UserResponseDTO = Depends(get_current_user)
) -> List[ProductResponseDTO]:
    return await index_service()


@product_router_v1.put(
    "/{product_id}",
    summary="Update product by id",
    description="Return some product by id updated",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=ProductResponseDTO,
    responses={
        401: {"model": ExceptionResponseDTO},
        404: {"model": ExceptionResponseDTO},
        409: {"model": ExceptionResponseDTO},
        429: {"model": ExceptionRateLimitResponseDTO}
    }
)
@limiter.limit(str(REQUEST_PER_MINUTES) + "/minute")
async def update(
    request: Request,
    product_id: str,
    productUpdateRequestDTO: ProductUpdateRequestDTO,
    user_logged: UserResponseDTO = Depends(get_current_user)
) -> ProductResponseDTO:
    return await update_service(product_id, productUpdateRequestDTO)


@product_router_v1.patch(
    "/{product_id}",
    summary="Upload banner to product by id",
    description="Return some product by id with uploaded banner with success",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=ProductResponseDTO,
    responses={
        401: {"model": ExceptionResponseDTO},
        404: {"model": ExceptionResponseDTO},
        406: {"model": ExceptionResponseDTO},
        429: {"model": ExceptionRateLimitResponseDTO}
    }
)
@limiter.limit(str(REQUEST_PER_MINUTES) + "/minute")
async def upload(
    request: Request,
    product_id: str,
    banner: UploadFile,
    user_logged: UserResponseDTO = Depends(get_current_user)
) -> ProductResponseDTO:
    return await upload_service(product_id, banner)


@product_router_v1.delete(
    "/{product_id}",
    summary="Delete some product by id",
    description="Delete some product by id with success",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: {"model": ExceptionResponseDTO},
        404: {"model": ExceptionResponseDTO},
        429: {"model": ExceptionRateLimitResponseDTO}
    }
)
@limiter.limit(str(REQUEST_PER_MINUTES) + "/minute")
async def destroy(
    request: Request,
    product_id: str,
    user_logged: UserResponseDTO = Depends(get_current_user)
) -> None:
    return await destroy_service(product_id)
