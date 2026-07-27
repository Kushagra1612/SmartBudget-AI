from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):

    full_name: str = Field(
        min_length=2,
        max_length=100,
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=100,
    )


class UserResponse(BaseModel):

    id: str

    full_name: str

    email: EmailStr

    model_config = {
        "from_attributes": True
    }