# Design – Technology Stack

## Tech Stack
- **Backend**: FastAPI (Python 3.12+)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Authentication**: JWT (PyJWT)
- **Validation**: Pydantic
- **Testing**: pytest, pytest-asyncio, coverage tools

## Testing & Quality Plan
- Coverage goals: 90%+ (critical features 100%)
- Unit tests for models, services, utilities
- Integration tests for all endpoints
- End-to-end regression tests
- Fixtures for reusable test data
- Pre-commit checks: Black, Flake8, mypy, isort

## Roadmap & Milestones
- Step 1: Documentation approval
- Step 2: Repo setup & docs migration
- Step 3: Implementation (auth, tasks, tests)
- Release: QA & deployment

## Glossary
- **JWT**: JSON Web Token, authentication
- **CRUD**: Create, Read, Update, Delete
- **ORM**: Object Relational Mapping
- **Pydantic**: Data validation
- **Alembic**: Database schema migration
