from pydantic import (
    BaseModel,
    EmailStr,
    Field
)


class CustomerCreate(BaseModel):

    name: str = Field(..., min_length=3)

    email: EmailStr

    phone: str = Field(..., min_length=10, max_length=10)

    address: str = Field(..., min_length=5)
