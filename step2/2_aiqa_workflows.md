
---

### `docs/step2/2_aiqa_workflows.md`

```markdown
# Step 2 — AI/QA Workflows

This document outlines developer workflows for code quality and consistency.

---

## Pre-commit Hooks
- **black** → enforce consistent formatting
- **isort** → organize imports
- **flake8** → linting
- **mypy** → type checking (configured in later steps)

Configured via `.pre-commit-config.yaml`.

---

## Testing
- **pytest** as test runner
- `tests/` directory already scaffolded
- Supports unit, integration, and API tests

---

## Code Quality Philosophy
- All code must follow **layered boundaries** (no circular imports, no business logic in API)
- Enforce strict typing (mypy)
- Use docstrings for all public functions and modules

---

## Developer Workflow
1. Write tests first (TDD encouraged)
2. Run `pytest` locally
3. Commit → pre-commit hooks auto-run
4. CI pipeline runs tests, lint, type-checking

---

## Outcome
By the end of Step 2:
- Codebase is **quality-gated**  
- Contributors cannot push poorly formatted or untyped code  
- Tests are integrated into every change
