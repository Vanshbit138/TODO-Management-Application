# Step 2 — Project Structure

This project follows a layered architecture to ensure maintainability, testability, and scalability.

```
src/
  api/                  # API Layer: FastAPI app and route handlers
    main.py             # Application entrypoint (app creation and router include)
    routers/
      auth.py           # Authentication endpoints
      task.py           # Task management endpoints
  core/                 # Core configuration and cross-cutting concerns
    config.py           # Pydantic settings, env config
    container.py        # Dependency injection wiring
    database.py         # SQLAlchemy engine/session lifecycle
    interfaces.py       # Abstract base classes (repositories/services)
  models/               # ORM entities (SQLAlchemy models)
    user.py             # User entity
    task.py             # Task entity
  repositories/         # Data access layer (DAL)
    user_repository.py  # User persistence operations
    task_repository.py  # Task persistence operations
  services/             # Business logic layer (domain/application services)
    authentication/
      auth_service.py       # JWT auth flows
      password_service.py   # Password hashing/validation
    task_management/
      task_service.py       # Task business rules
```


---

## Folder Purposes

### `core/`
- **Purpose:** Application composition and cross-cutting concerns
- **Keep:** configuration objects, DI container, DB setup, base classes, security utils
- **Avoid:** business rules, API route code, ORM entity definitions

### `api/`
- **Purpose:** HTTP layer exposing endpoints and request/response boundaries
- **Keep:** FastAPI app, routers, request/response schemas (DTOs)
- **Avoid:** persistence queries, heavy business logic

### `models/`
- **Purpose:** Database entities and ORM mapping
- **Keep:** SQLAlchemy models, table metadata, relationship declarations
- **Avoid:** request/response schemas, I/O code, business workflows

### `repositories/`
- **Purpose:** Data access abstractions and implementations
- **Keep:** CRUD operations, query methods, transaction boundaries
- **Avoid:** HTTP specifics, unrelated business logic

### `services/`
- **Purpose:** Orchestrate business use-cases independent of transport and persistence
- **Keep:** domain logic, validation rules, orchestration across repositories
- **Avoid:** direct SQL, HTTP request parsing, framework-specific code

### `tests/`
- **Purpose:** Ensure code correctness and regression prevention
- **Keep:** fixtures, unit tests, API tests, repository tests
- **Avoid:** production-only code

---

## Import Direction (Dependency Rule)
- **api → services → repositories → models**
- `core` is used by all layers but must not depend on other layers

---

## Naming Conventions
- Modules: nouns (`models`, `repositories`)
- Services: verbs/verb-phrases (`task_service`)
- Functions: small, composable
- Errors: raised and handled at layer boundaries