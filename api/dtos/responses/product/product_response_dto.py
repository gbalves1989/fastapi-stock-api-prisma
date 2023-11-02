from pydantic import BaseModel


class CategoryResponseDTO(BaseModel):
    id: str
    name: str


class ProductResponseDTO(BaseModel):
    id: str
    name: str
    description: str
    banner: str
    category: CategoryResponseDTO


class ProductNameResponseDTO(BaseModel):
    id: str
    name: str
    description: str
    banner: str
