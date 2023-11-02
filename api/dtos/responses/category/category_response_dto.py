from pydantic import BaseModel
from typing import List


class CategoryResponseDTO(BaseModel):
    id: str
    name: str


class ProductResponseDTO(BaseModel):
    id: str
    name: str
    description: str
    banner: str


class CategoryDetailResponseDTO(CategoryResponseDTO):
    products: List[ProductResponseDTO]
