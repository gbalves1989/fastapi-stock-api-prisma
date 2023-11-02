from fastapi import APIRouter
from core.config import API_VERSION
from api.endpoints.v1 import (
    category_endpoint_v1,
    product_endpoint_v1,
    user_endpoint_v1
)

api_router = APIRouter()

if API_VERSION == "v1":
    api_router.include_router(
        user_endpoint_v1.user_router_v1,
        prefix="/users",
        tags=["Users"]
    )
    api_router.include_router(
        category_endpoint_v1.category_router_v1,
        prefix="/categories",
        tags=["Categories"]
    )
    api_router.include_router(
        product_endpoint_v1.product_router_v1,
        prefix="/products",
        tags=["Products"]
    )
