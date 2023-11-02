from pydantic import BaseModel


class CategoryCreateRequestDTO(BaseModel):
    name: str
