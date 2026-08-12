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


from uuid import UUID

class UserResponse(BaseModel):

    id: UUID

    full_name: str

    email: EmailStr

    model_config = {
        "from_attributes": True
    }