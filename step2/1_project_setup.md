# Step 2 — Project Setup

This step defines the initial backend project scaffolding using FastAPI, SQLAlchemy, Alembic, and pytest. No business logic is implemented; only structure and documentation.

## Goals
- Create a modular, layered architecture following SOLID and clean architecture principles
- Prepare directories for API, Core, Models, Repositories, Services, and Tests
- Add environment template and dependency files

## Tech Stack
- Python 3.12+
- FastAPI, Uvicorn
- SQLAlchemy 2.x, Alembic
- PostgreSQL
- Pydantic v2, pydantic-settings
- PyJWT/Jose, Passlib
- pytest

## How to run (later steps)
- Create virtualenv, install `requirements/requirements.txt` and `dev_requirements.txt`
- Copy `env.example` to `.env` and adjust values
- Run app via `uvicorn src.api.main:app --reload` (after implementation in next steps)

