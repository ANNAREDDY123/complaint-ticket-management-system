from pydantic import (
    BaseModel,
    Field
)


class TicketCreate(BaseModel):

    customer_id: int

    title: str = Field(..., min_length=5)

    description: str = Field(..., min_length=10)

    priority: str

    category: str
