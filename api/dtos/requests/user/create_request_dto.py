from pydantic import BaseModel, EmailStr


class UserCreateRequestDTO(BaseModel):
    name: str
    email: EmailStr
    password: str
    confirm_password: str
