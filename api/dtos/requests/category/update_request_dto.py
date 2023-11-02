from pydantic import BaseModel


class CategoryUpdateRequestDTO(BaseModel):
    name: str
