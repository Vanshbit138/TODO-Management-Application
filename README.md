# TODO Management Application

This repository contains a backend service built with FastAPI, structured using a layered architecture to enable clean separation of concerns and scalability.

## Step 2 Overview
Step 2 introduces the initial project structure only (no business logic yet). We scaffold the following layers under `src/`:

- `api/`: FastAPI application and HTTP route handlers
- `core/`: configuration, dependency injection container, database setup, base interfaces
- `models/`: SQLAlchemy ORM entities
- `repositories/`: data access layer (CRUD/query operations)
- `services/`: business logic (authentication, task management)

Refer to the Step 2 docs:
- `step2/1_project_setup.md`
- `step2/2_aiqa_workflows.md`
- `step2/3_project_structure.md`
- `step2/4_data_modeling.md`

## Getting Started (after implementation phases)
1. Create a virtual environment with Python 3.12+
2. `pip install -r requirements/requirements.txt -r dev_requirements.txt`
3. Copy `env.example` to `.env` and set values
4. Run: `uvicorn src.api.main:app --reload`

Note: At Step 2, modules contain only docstrings to describe responsibilities. Implementation happens in later steps.
