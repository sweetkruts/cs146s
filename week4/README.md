# Week 4: The Autonomous Coding Agent IRL

## Assignment Completed 

This project implements **8 automations** for Claude Code to enhance developer workflows:

### Automations Created

#### 1. Custom Slash Commands (3)
- **`/test-suite`** - Run tests with coverage analysis and actionable feedback
- **`/docs-sync`** - Sync API documentation with OpenAPI spec
- **`/add-endpoint`** - Guided TDD workflow for adding new endpoints

Located in: `.claude/commands/`

#### 2. CLAUDE.md Guidance Files (2)
- **Root CLAUDE.md** - Repository-wide context and patterns
- **Week 4 CLAUDE.md** - Project-specific quick reference

#### 3. SubAgent Configurations (3)
- **TestAgent** - Testing specialist (test creation and coverage)
- **CodeAgent** - Implementation specialist (feature development)
- **DocsAgent** - Documentation specialist (docs maintenance)

Located in: `.claude/subagents/`

### Application Enhancements

Using the automations above, the starter application was enhanced with:

#### New Features
-  **PUT /notes/{note_id}** - Update existing notes (full or partial)
-  **DELETE /notes/{note_id}** - Delete notes
-  Request validation on all endpoints
-  Frontend edit/delete functionality
-  Comprehensive API documentation

#### Test Coverage
- **10 tests** - All passing
- **7 new test functions** added
- **100% coverage** on new endpoints

#### Documentation
- Complete `docs/API.md` with 9 endpoints documented
- Examples and error codes for all endpoints

### Quick Start

```bash
# Activate conda environment
conda activate cs146s

# Navigate to week4
cd week4/

# Run the application
make run

# Run tests
make test

# Format code
make format
```

Visit:
- **Frontend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **API Reference**: See `docs/API.md`

### Key Files

- **Automations**: `.claude/commands/*.md` and `.claude/subagents/*.md`
- **Guidance**: `CLAUDE.md` (root and week4)
- **Writeup**: `week4/writeup.md` (comprehensive documentation)
- **API Docs**: `week4/docs/API.md`

