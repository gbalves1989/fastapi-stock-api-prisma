from pydantic import BaseModel


class ProductUpdateRequestDTO(BaseModel):
    name: str
    description: str
