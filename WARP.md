# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Repository Overview

Educational repository for CS146S: The Modern Software Developer at Stanford (Fall 2025). Contains weekly assignments focused on AI-assisted development practices, LLM prompting, FastAPI applications, and autonomous coding agents.

## Environment Setup

```bash
# Create conda environment (Python 3.12)
conda create -n cs146s python=3.12 -y
conda activate cs146s

# Install dependencies with Poetry
poetry install --no-interaction
```

## Common Commands

### Testing
```bash
# From week4/ or week5/ directory
make test                    # Run all tests
PYTHONPATH=. pytest -v backend/tests                    # Verbose output
PYTHONPATH=. pytest backend/tests/test_notes.py -v      # Single test file
PYTHONPATH=. pytest backend/tests --cov=backend/app     # With coverage
```

### Running Applications
```bash
# Week 2 (Action Item Extractor)
cd week2
poetry run uvicorn week2.app.main:app --reload

# Week 3 (Spotify MCP Server) - requires Ollama
cd week3
python -m server.main

# Week 4/5 (Full-stack starter)
cd week4   # or week5
make run
# Visit http://localhost:8000
```

### Code Quality
```bash
# From week4/ or week5/ directory
make format    # Format with black + ruff
make lint      # Check with ruff only
```

## Architecture Patterns

### Week 2-5: FastAPI Full-Stack Pattern

**Structure:**
```
weekN/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app + lifespan
│   │   ├── models.py        # SQLAlchemy ORM models
│   │   ├── schemas.py       # Pydantic request/response schemas
│   │   ├── db.py            # Database setup + dependency injection
│   │   ├── routers/         # API endpoint modules (notes, action_items)
│   │   └── services/        # Business logic (e.g., extract.py)
│   └── tests/
│       ├── conftest.py      # Pytest fixtures (client, db_session)
│       └── test_*.py        # Test files
├── frontend/                # Static HTML/CSS/JS served by FastAPI
├── data/
│   ├── app.db               # SQLite database (auto-created)
│   └── seed.sql             # Initial data (auto-applied)
└── Makefile
```

**Key Architectural Principles:**

1. **Router Pattern**: Each resource has its own router file (e.g., `routers/notes.py`) with prefix and tags
   ```python
   router = APIRouter(prefix="/notes", tags=["notes"])
   ```

2. **Dependency Injection**: Database sessions injected via FastAPI Depends
   ```python
   def endpoint(db: Session = Depends(get_db)):
   ```

3. **Schema Separation**: Distinct Pydantic models for Create/Read/Update operations
   - `NoteCreate`, `NoteRead`, `NoteUpdate` in `schemas.py`

4. **Database Layer**: SQLAlchemy ORM with automatic initialization on startup
   - Models defined in `models.py` (inherit from `Base`)
   - Seeding applied via `apply_seed_if_needed()` in startup event

5. **Static Frontend**: Served directly by FastAPI via `StaticFiles` mount
   - No Node.js build process required
   - Frontend at `/`, API docs at `/docs`

### Week 1: LLM Prompting Patterns

Standalone Python scripts demonstrating prompting techniques:
- `chain_of_thought.py` - Step-by-step reasoning
- `k_shot_prompting.py` - Few-shot examples
- `self_consistency_prompting.py` - Multiple reasoning paths
- `reflexion.py` - Self-reflection and refinement
- `rag.py` - Retrieval-augmented generation
- `tool_calling.py` - Function/tool usage

Run directly: `python week1/chain_of_thought.py`

### Week 3: MCP Server Architecture

FastAPI server wrapping external APIs (Spotify) with OAuth2:
- HTTP transport for MCP protocol
- Separate authentication layers (MCP API key + OAuth2)
- Tool definitions in `server/mcp_tools.py`
- API client logic in `server/spotify_client.py`

## Development Workflow

### Test-Driven Development (TDD)
1. Write failing test in `backend/tests/test_*.py`
2. Run `make test` to confirm failure
3. Implement feature to pass test
4. Run `make test` again to verify
5. Run `make format` before committing

### Adding New API Endpoints
1. Define Pydantic schemas in `schemas.py` (request/response models)
2. Add SQLAlchemy model to `models.py` if new resource
3. Create/update router in `routers/[resource].py`
4. Include router in `main.py` if new
5. Write tests in `tests/test_[resource].py` (success + error cases)
6. Run tests, implement feature, format code

**Router Template:**
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..schemas import ResourceCreate, ResourceRead

router = APIRouter(prefix="/resource", tags=["resource"])

@router.post("/", response_model=ResourceRead, status_code=201)
def create_resource(
    resource: ResourceCreate,
    db: Session = Depends(get_db)
) -> ResourceRead:
    # Implementation with error handling
    pass
```

### Test Patterns
- **Fixtures**: `client` (TestClient), `db_session` (in-memory DB) in `conftest.py`
- **Test naming**: `test_endpoint_success`, `test_endpoint_not_found`, `test_endpoint_validation`
- **Structure**: Setup → Execute → Assert
- **Error cases**: Always test 404, 400, 422 scenarios
- **Coverage goal**: >80% for new code

## Code Quality Standards

- **Type hints**: Required on all function parameters and return types
- **HTTP status codes**: Use appropriate codes (200, 201, 204, 400, 404, 422)
- **Error handling**: Raise `HTTPException` with descriptive messages
- **Formatting**: Black (line length 100) + Ruff linting
- **Pre-commit hooks**: Available in week4/week5 (optional but recommended)

## Configuration

- **Poetry**: Dependency management (`pyproject.toml`)
- **Environment**: `.env` files in project directories (week2, week3)
- **Database**: SQLite, auto-created in `data/app.db`
- **Python version**: 3.12 (3.10+ compatible)

## Testing Framework

- **pytest**: Test runner
- **httpx**: TestClient via FastAPI
- **SQLAlchemy**: In-memory test databases
- **Fixtures**: Defined in `conftest.py` for reusable test dependencies

## Important Files

- **Root README.md**: Setup instructions and environment configuration
- **pyproject.toml**: Global Poetry dependencies (FastAPI, SQLAlchemy, pytest, black, ruff)
- **CLAUDE.md**: Additional guidance for Claude Code agents (week 4 specific patterns)
- **.claude/**: Custom commands and SubAgent configurations (week 4)

## Week-Specific Notes

### Week 2: Action Item Extractor
- Dual extraction methods: heuristic + LLM (Ollama)
- Requires Ollama running: `ollama pull llama3.1:8b`
- Run from root: `poetry run uvicorn week2.app.main:app --reload`

### Week 3: Spotify MCP Server
- Requires Spotify Developer credentials in `.env`
- OAuth2 flow at `/auth/login` before using tools
- MCP endpoints: `/mcp/list_tools`, `/mcp/call_tool`

### Week 4/5: Full-Stack Starter
- Identical structure, week 5 is clean slate
- Week 4 includes comprehensive automation examples
- Seeding automatic on startup
- Frontend updates require no build step

## Common Pitfalls

- **PYTHONPATH**: Must set `PYTHONPATH=.` when running tests/app from week directories
- **Database locks**: Stop all running instances before restarting
- **Import paths**: Use relative imports within app (`from ..db import get_db`)
- **Router registration**: Don't forget `app.include_router()` in `main.py`
- **Test isolation**: Use `db_session` fixture, not global `get_db`

## Quick Reference

**Run server**: `cd week4 && make run` (or week5)
**Run tests**: `cd week4 && make test`
**Format code**: `cd week4 && make format`
**API docs**: http://localhost:8000/docs (when running)
**Test coverage**: `PYTHONPATH=. pytest backend/tests --cov=backend/app --cov-report=term-missing`
