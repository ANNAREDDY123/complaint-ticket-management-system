from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)

from database import Base


class Ticket(Base):

    __tablename__ = "tickets"

    id = Column(
        Integer,
        primary_key=True
    )

    customer_id = Column(
        Integer,
        ForeignKey("customers.id")
    )

    assigned_agent_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    title = Column(String)

    description = Column(String)

    priority = Column(String)

    category = Column(String)

    status = Column(
        String,
        default="Open" )
