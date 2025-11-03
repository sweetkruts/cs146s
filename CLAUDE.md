# Repository Guide for Claude Code

## Repository Overview
This is a modern software development course repository containing weekly assignments focused on AI-assisted development practices.

## Active Development: Week 4
Current focus is on `week4/` - a full-stack starter application serving as a "developer's command center" for notes and action items.

## Week 4 Application Architecture

### Structure
```
week4/
├── backend/           # FastAPI application
│   ├── app/
│   │   ├── main.py       # App entry point
│   │   ├── models.py     # SQLAlchemy models
│   │   ├── schemas.py    # Pydantic schemas
│   │   ├── db.py         # Database setup
│   │   ├── routers/      # API endpoints
│   │   └── services/     # Business logic
│   └── tests/         # pytest test suite
├── frontend/          # Static HTML/JS/CSS
├── data/             # SQLite database
└── docs/             # Documentation and tasks
```

### How to Run
```bash
cd week4/
make run          # Start server (http://localhost:8000)
make test         # Run tests
make format       # Format with black + ruff
make lint         # Check with ruff
```

### Database
- SQLite with SQLAlchemy ORM
- Auto-seeded from `data/seed.sql` on startup
- Models: `Note`, `ActionItem`

## Development Workflow Standards

### When Adding New Features
1. **Test-Driven Development (TDD)**
   - Write failing test first in `backend/tests/`
   - Implement feature to make test pass
   - Run full test suite to ensure no regressions

2. **Code Quality**
   - Use type hints for all function parameters and returns
   - Follow existing patterns in the codebase
   - Keep functions focused and single-purpose
   - Use proper HTTP status codes (200, 201, 404, 400, etc.)

3. **Testing Requirements**
   - Unit tests for business logic in `services/`
   - Integration tests for API endpoints
   - Test both success and failure cases
   - Aim for >80% code coverage

4. **Formatting/Linting**
   - Always run `make format` before committing
   - Ensure `make lint` passes with no errors
   - black for formatting, ruff for linting
   - Pre-commit hooks available (optional)

### When Adding API Endpoints
1. Define schemas in `schemas.py` (request/response models)
2. Implement route in appropriate router (`routers/notes.py` or `routers/action_items.py`)
3. Add database operations using SQLAlchemy
4. Include proper error handling with HTTPException
5. Write tests in corresponding test file
6. Update frontend if user-facing (optional)
7. Run `/docs-sync` to update API documentation

### Router Patterns
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db

router = APIRouter(prefix="/resource", tags=["resource"])

@router.get("/", response_model=list[ResourceRead])
def list_resources(db: Session = Depends(get_db)) -> list[ResourceRead]:
    # Implementation
    pass
```

### Test Patterns
```python
def test_endpoint_success(client, db_session):
    # Setup
    # Execute
    response = client.get("/endpoint")
    # Assert
    assert response.status_code == 200
    assert "field" in response.json()

def test_endpoint_not_found(client, db_session):
    response = client.get("/endpoint/999")
    assert response.status_code == 404
```

## Available Custom Commands

### `/test-suite [optional: test path]`
Runs tests with coverage analysis and provides actionable feedback on failures.

### `/docs-sync`
Syncs API documentation with OpenAPI spec, identifying new/changed/removed endpoints.

### `/add-endpoint [resource] [method] [path]`
Guided TDD workflow to add a new API endpoint with tests and proper error handling.

## Safety Guidelines

### Safe Operations
- Reading any file in the repository
- Running tests (`make test`)
- Running linters (`make lint`, `make format`)
- Starting the dev server (`make run`)
- Creating/updating documentation files
- Adding tests

### Operations Requiring Care
- Modifying database models (requires migration consideration)
- Changing schemas (may break frontend)
- Deleting files
- Modifying test fixtures

### Never Do
- Force push to main branch
- Skip tests or linting
- Hard-code secrets or API keys
- Commit without running tests
- Remove existing tests

## SubAgent Workflows

### TestAgent Role
**Focus**: Test creation, verification, and coverage analysis
**Tools**: pytest, coverage.py
**Workflow**:
1. Understand feature requirements
2. Write comprehensive tests (success + failure cases)
3. Verify tests fail appropriately (TDD)
4. After CodeAgent implements, verify tests pass
5. Check coverage and suggest additional tests

### CodeAgent Role
**Focus**: Implementation of application logic
**Tools**: FastAPI, SQLAlchemy, Pydantic
**Workflow**:
1. Receive failing tests from TestAgent
2. Implement minimal code to pass tests
3. Follow existing code patterns
4. Use proper type hints and error handling
5. Run linter and fix issues

### DocsAgent Role
**Focus**: Documentation maintenance and API drift detection
**Tools**: OpenAPI spec, markdown
**Workflow**:
1. Monitor OpenAPI spec changes
2. Update API.md with endpoint details
3. Identify undocumented or changed endpoints
4. Maintain TASKS.md with TODOs
5. Ensure examples are up-to-date

## Common Tasks Reference

### Add CRUD operations for a resource
1. Create model in `models.py`
2. Create schemas in `schemas.py` (Create, Read, Update)
3. Create router in `routers/[resource].py`
4. Include router in `main.py`
5. Write tests in `tests/test_[resource].py`
6. Update frontend if needed

### Add search/filter functionality
1. Extend existing GET endpoint with query parameters
2. Use SQLAlchemy filters (`.where()`, `.contains()`, etc.)
3. Test with various query combinations
4. Update frontend search UI

### Add validation rules
1. Use Pydantic field validators in schemas
2. Use `Field(min_length=X)` for string constraints
3. Test validation failures return 422 status

## Files to Avoid Modifying
- `pyproject.toml`, `poetry.lock` (dependency management)
- `.git/` (version control internals)
- `__pycache__/`, `*.pyc` (Python cache)
- `data/app.db` (runtime database - regenerated)

## Quick Reference

**Entry point**: `backend/app/main.py`
**API docs**: http://localhost:8000/docs (when running)
**Frontend**: http://localhost:8000
**Test command**: `PYTHONPATH=. pytest backend/tests -v`
**Coverage**: `PYTHONPATH=. pytest backend/tests --cov=backend/app`



