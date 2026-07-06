from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal

from models.ticket import Ticket
from models.customer import Customer
from models.user import User

from schemas.ticket import TicketCreate

from services.ticket_service import (
    valid_priority,
    valid_status
)

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/")
def create_ticket(
    ticket: TicketCreate,
    db: Session = Depends(get_db)
):

    customer = db.query(Customer).filter(
        Customer.id == ticket.customer_id
    ).first()

    if not customer:

        raise HTTPException(
            status_code=404,
            detail="Customer not found."
        )

    if not valid_priority(ticket.priority):

        raise HTTPException(
            status_code=400,
            detail="Invalid ticket priority."
        )

    new_ticket = Ticket(
        customer_id=ticket.customer_id,
        title=ticket.title,
        description=ticket.description,
        priority=ticket.priority,
        category=ticket.category,
        status="Open"
    )

    db.add(new_ticket)

    db.commit()

    db.refresh(new_ticket)

    return new_ticket


@router.get("/")
def get_tickets(
    title: str = None,
    priority: str = None,
    status: str = None,
    customer_id: int = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    query = db.query(Ticket)

    if title:
        query = query.filter(
            Ticket.title.contains(title)
        )

    if priority:
        query = query.filter(
            Ticket.priority == priority
        )

    if status:
        query = query.filter(
            Ticket.status == status
        )

    if customer_id:
        query = query.filter(
            Ticket.customer_id == customer_id
        )

    total = query.count()

    tickets = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total_records": total,
        "current_page": page,
        "limit": limit,
        "data": tickets
    }


@router.get("/{ticket_id}")
def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db)
):

    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()

    if not ticket:

        raise HTTPException(
            status_code=404,
            detail="Ticket not found."
        )

    return ticket


@router.put("/{ticket_id}")
def update_ticket(
    ticket_id: int,
    ticket: TicketCreate,
    db: Session = Depends(get_db)
):

    db_ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()

    if not db_ticket:

        raise HTTPException(
            status_code=404,
            detail="Ticket not found."
        )

    if db_ticket.status == "Closed":

        raise HTTPException(
            status_code=400,
            detail="Closed tickets cannot be updated."
        )

    db_ticket.title = ticket.title
    db_ticket.description = ticket.description
    db_ticket.priority = ticket.priority
    db_ticket.category = ticket.category

    db.commit()

    return {
        "message": "Ticket updated successfully."
    }


@router.delete("/{ticket_id}")
def delete_ticket(
    ticket_id: int,
    db: Session = Depends(get_db)
):

    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()

    if not ticket:

        raise HTTPException(
            status_code=404,
            detail="Ticket not found."
        )

    db.delete(ticket)

    db.commit()

    return {
        "message": "Ticket deleted successfully."
    }


@router.post("/{ticket_id}/assign/{agent_id}")
def assign_ticket(
    ticket_id: int,
    agent_id: int,
    db: Session = Depends(get_db)
):

    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()

    if not ticket:

        raise HTTPException(
            status_code=404,
            detail="Ticket not found."
        )

    agent = db.query(User).filter(
        User.id == agent_id
    ).first()

    if not agent:

        raise HTTPException(
            status_code=404,
            detail="Support agent not found."
        )

    if ticket.assigned_agent_id:

        raise HTTPException(
            status_code=400,
            detail="Ticket is already assigned."
        )

    ticket.assigned_agent_id = agent_id
    ticket.status = "In Progress"

    db.commit()

    return {
        "message": "Ticket assigned successfully."
    }


@router.get("/agents/{agent_id}")
def agent_tickets(
    agent_id: int,
    db: Session = Depends(get_db)
):

    return db.query(Ticket).filter(
        Ticket.assigned_agent_id == agent_id
    ).all()
