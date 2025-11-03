# Week 4 Development Guide

## Quick Start
```bash
# From week4/ directory
make run          # Start server
make test         # Run tests
make format       # Format code
make lint         # Check linting
```

## Project Context
Full-stack developer command center with notes and action items. FastAPI backend, static frontend, SQLite database.

## When Working on Features
1. Write test first (TDD)
2. Implement feature
3. Run `make test` 
4. Run `make format`
5. Verify manually at http://localhost:8000

## File Organization
- `backend/app/routers/` - API endpoints
- `backend/app/services/` - Business logic
- `backend/tests/` - Test suite
- `frontend/` - Static UI files
- `docs/TASKS.md` - Feature backlog

## Custom Commands Available
- `/test-suite` - Run tests with coverage
- `/docs-sync` - Update API documentation
- `/add-endpoint` - Add new endpoint with TDD

## Type Hints Required
All functions must have type hints for parameters and return values.

## Testing Standards
- Test both success and error cases
- Use fixtures from `conftest.py`
- Aim for >80% coverage



