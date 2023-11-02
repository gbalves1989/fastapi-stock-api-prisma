from pydantic import BaseModel, EmailStr


class UserUpdateRequestDTO(BaseModel):
    name: str
    password: str
    confirm_password: str
