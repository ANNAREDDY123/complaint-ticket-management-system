from sqlalchemy import Column, Integer, String

from database import Base


class Customer(Base):

    __tablename__ = "customers"

    id = Column(
        Integer,
        primary_key=True
    )

    name = Column(String)

    email = Column(
        String,
        unique=True
    )

    phone = Column(String)

    address = Column(String)
