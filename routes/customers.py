from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.customer import Customer
from schemas.customer import CustomerCreate

from services.ticket_service import valid_phone

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/")
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(Customer).filter(
        Customer.email == customer.email
    ).first()

    if existing:

        raise HTTPException(
            status_code=400,
            detail="Customer email already exists."
        )

    if not valid_phone(customer.phone):

        raise HTTPException(
            status_code=400,
            detail="Phone number must contain exactly 10 digits."
        )

    new_customer = Customer(
        name=customer.name,
        email=customer.email,
        phone=customer.phone,
        address=customer.address
    )

    db.add(new_customer)

    db.commit()

    db.refresh(new_customer)

    return new_customer


@router.get("/")
def get_customers(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    query = db.query(Customer)

    total = query.count()

    customers = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total_records": total,
        "current_page": page,
        "limit": limit,
        "data": customers
    }


@router.get("/{customer_id}")
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):

    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not customer:

        raise HTTPException(
            status_code=404,
            detail="Customer not found."
        )

    return customer


@router.put("/{customer_id}")
def update_customer(
    customer_id: int,
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):

    db_customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not db_customer:

        raise HTTPException(
            status_code=404,
            detail="Customer not found."
        )

    db_customer.name = customer.name
    db_customer.email = customer.email
    db_customer.phone = customer.phone
    db_customer.address = customer.address

    db.commit()

    return {
        "message": "Customer updated successfully."
    }


@router.delete("/{customer_id}")
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):

    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not customer:

        raise HTTPException(
            status_code=404,
            detail="Customer not found."
        )

    db.delete(customer)

    db.commit()

    return {
        "message": "Customer deleted successfully."
    }
