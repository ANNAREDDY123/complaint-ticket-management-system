# complaint-ticket-management-system
FastAPI Complaint &amp; Ticket Management System with JWT Authentication, Customer Management, Ticket Management, Ticket Assignment, Search, Reports, SQLAlchemy ORM, Pagination, Logging, and Docker Support.
# Complaint & Ticket Management System

## Features

- JWT Authentication
- Customer Management (CRUD)
- Ticket Management (CRUD)
- Ticket Assignment
- Search, Filter & Pagination
- SQLAlchemy ORM
- SQLite Database
- Docker Support
- Logging
- Basic Unit Tests

---

## Setup Instructions

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Project

```bash
uvicorn main:app --reload
```

Swagger URL

```
http://127.0.0.1:8000/docs
```

---

## Environment Variables

```
SECRET_KEY=complaint_secret_key
ALGORITHM=HS256
```

---

## API Flow

1. Register
2. Login
3. Create Customer
4. Create Ticket
5. Assign Ticket
6. Update Ticket
7. Search & Reports

---

## Docker Deployment

```bash
docker build -t complaint-ticket .
docker run -p 8000:8000 complaint-ticket
```

---

## Assumptions

- Customer email is unique.
- One ticket can be assigned to only one support agent.
- Closed tickets cannot be updated.
- Pagination is supported for listing APIs.
