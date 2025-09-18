# Step 2 — Project Setup

This step defines the initial backend project scaffolding using FastAPI, SQLAlchemy, Alembic, and pytest.  
No business logic is implemented yet; only structure and documentation. This allows contributors to understand the architecture and start contributing in a consistent way.

---

## Goals
- Establish a **modular, layered architecture** following SOLID and Clean Architecture principles
- Prepare directories for API, Core, Models, Repositories, Services, and Tests
- Provide environment templates, dependency files, and tooling setup
- Ensure code quality pipelines are ready (testing, linting, type checking)

---

## Tech Stack
- **Python** 3.12+
- **FastAPI** + Uvicorn (ASGI app & API layer)
- **SQLAlchemy 2.x** ORM + Alembic migrations
- **PostgreSQL** (primary database)
- **Pydantic v2 + pydantic-settings** (data validation & config management)
- **PyJWT/Jose** + **Passlib** (authentication/crypto)
- **pytest** (unit/integration testing)

---

## Setup Instructions (later steps)
1. Create a virtualenv with Python 3.12+
2. Install dependencies:  
   ```bash
   pip install -r requirements/requirements.txt