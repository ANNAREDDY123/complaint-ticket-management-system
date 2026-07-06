CREATE TABLE users(
    id INTEGER PRIMARY KEY,
    username VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    role VARCHAR(50)
);

CREATE TABLE customers(
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    address VARCHAR(255)
);

CREATE TABLE tickets(
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    assigned_agent_id INTEGER,
    title VARCHAR(255),
    description TEXT,
    priority VARCHAR(50),
    category VARCHAR(100),
    status VARCHAR(50)
);
