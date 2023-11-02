from pydantic import BaseModel, EmailStr


class UserLoginRequestDTO(BaseModel):
    email: EmailStr
    password: str
