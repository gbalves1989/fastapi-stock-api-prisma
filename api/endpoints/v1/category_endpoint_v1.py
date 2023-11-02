from typing import List
from fastapi import APIRouter, status, Depends, Request

from slowapi import Limiter
from slowapi.util import get_remote_address

from api.services.category_service import (
    store_service,
    show_service,
    update_service,
    index_service,
    destroy_service
)
from api.dtos.requests.category.create_request_dto import CategoryCreateRequestDTO
from api.dtos.requests.category.update_request_dto import CategoryUpdateRequestDTO
from api.dtos.responses.category.category_response_dto import (
    CategoryResponseDTO,
    CategoryDetailResponseDTO
)
from api.dtos.responses.exception_response_dto import (
    ExceptionResponseDTO,
    ExceptionRateLimitResponseDTO
)
from api.dtos.responses.user.user_response_dto import UserResponseDTO

from core.authentication.deps import get_current_user
from core.config import REQUEST_PER_MINUTES

category_router_v1 = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@category_router_v1.post(
    "/",
    summary="Create a new category",
    description="Return a new category created with success",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoryResponseDTO,
    responses={
        401: {"model": ExceptionResponseDTO},
        409: {"model": ExceptionResponseDTO},
        429: {"model": ExceptionRateLimitResponseDTO}
    }
)
@limiter.limit(str(REQUEST_PER_MINUTES) + "/minute")
async def store(
    request: Request,
    categoryCreateRequestDTO: CategoryCreateRequestDTO,
    user_logged: UserResponseDTO = Depends(get_current_user)
) -> CategoryResponseDTO:
    return await store_service(categoryCreateRequestDTO)


@category_router_v1.get(
    "/{category_id}",
    summary="Get some category by id",
    description="Return some category by id",
    status_code=status.HTTP_200_OK,
    response_model=CategoryDetailResponseDTO,
    responses={
        401: {"model": ExceptionResponseDTO},
        404: {"model": ExceptionResponseDTO},
        429: {"model": ExceptionRateLimitResponseDTO}
    }
)
@limiter.limit(str(REQUEST_PER_MINUTES) + "/minute")
async def show(
    request: Request,
    category_id: str,
    user_logged: UserResponseDTO = Depends(get_current_user)
) -> CategoryDetailResponseDTO:
    return await show_service(category_id)


@category_router_v1.get(
    "/",
    summary="List of categories",
    description="Return some list of categories",
    status_code=status.HTTP_200_OK,
    response_model=List[CategoryResponseDTO],
    responses={
        401: {"model": ExceptionResponseDTO},
        429: {"model": ExceptionRateLimitResponseDTO}
    }
)
@limiter.limit(str(REQUEST_PER_MINUTES) + "/minute")
async def index(
    request: Request,
    user_logged: UserResponseDTO = Depends(get_current_user)
) -> List[CategoryResponseDTO]:
    return await index_service()


@category_router_v1.put(
    "/{category_id}",
    summary="Update some category by id",
    description="Return some category by id updated",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=CategoryDetailResponseDTO,
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
    category_id: str,
    categoryUpdateRequestDTO: CategoryUpdateRequestDTO,
    user_logged: UserResponseDTO = Depends(get_current_user)
) -> CategoryDetailResponseDTO:
    return await update_service(category_id, categoryUpdateRequestDTO)


@category_router_v1.delete(
    "/{category_id}",
    summary="Delete some category by id",
    description="Delete some category by id with success",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: {"model": ExceptionResponseDTO},
        404: {"model": ExceptionResponseDTO},
        422: {"model": ExceptionResponseDTO},
        429: {"model": ExceptionRateLimitResponseDTO}
    }
)
@limiter.limit(str(REQUEST_PER_MINUTES) + "/minute")
async def destroy(
    request: Request,
    category_id: str,
    user_logged: UserResponseDTO = Depends(get_current_user)
) -> None:
    return await destroy_service(category_id)
