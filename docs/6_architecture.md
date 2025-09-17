# Architecture & Workflow

##  System Architecture Diagram

The TODO Management Application follows a **modular, layered architecture** for scalability and maintainability.  

**Request Flow:**
1. Client (Web/Mobile) sends requests via REST API.  
2. Authentication middleware validates JWT tokens.  
3. Requests are routed to domain-specific services (Users, Tasks).  
4. Services use SQLAlchemy ORM to interact with PostgreSQL.  
5. Middleware and global error handling ensure security and consistent responses.  

![System Architecture](../assets/system_architecture.png)

---

## ERD / Data Model

The system uses a **normalized relational schema** with clear relationships.  

- **Users Table** → Stores user credentials & account metadata.  
- **Tasks Table** → Stores personal TODO items with user ownership enforced.  
- Relationship: One user can own many tasks, but each task belongs to exactly one user.  

![Entity Relationship Diagram](../assets/erd.png)

---

## High-Level System Diagram

This diagram shows the **end-to-end workflow** of the system.  

- Client interacts with the **FastAPI backend**.  
- Authenticated requests are processed through routers, services, and data access layers.  
- PostgreSQL ensures secure, persistent data storage.  
- JWT authentication ensures user isolation and data privacy.  

![High Level System Architecture](../assets/high_system_architecture.png)
