# Multi-Agent Coordination Playbook

## Strategy Overview

Execute 4 independent tasks concurrently using separate Warp agent tabs with git worktrees to prevent conflicts.

## Selected Tasks (From TASKS.md)

We'll run these 4 self-contained tasks simultaneously:

### Agent 1: Notes CRUD Operations (Task #3)
**Difficulty:** Medium  
**Work on:** `worktree-agent1`

**Scope:**
- Add `PUT /notes/{id}` endpoint
- Add `DELETE /notes/{id}` endpoint
- Update schemas with validation
- Add tests for CRUD operations

**Why independent:** Focused on notes router only, minimal overlap with other tasks.

### Agent 2: Action Items Filtering (Task #4 - Partial)
**Difficulty:** Easy-Medium  
**Work on:** `worktree-agent2`

**Scope:**
- Add `GET /action-items?completed=true|false` filtering
- Update router with query parameters
- Add tests for filter behavior

**Why independent:** Only touches action_items router, no bulk operations to avoid complexity.

### Agent 3: Error Handling & Response Envelopes (Task #7)
**Difficulty:** Easy-Medium  
**Work on:** `worktree-agent3`

**Scope:**
- Add Pydantic validation constraints
- Create global exception handlers
- Implement consistent response envelopes
- Update tests for error cases

**Why independent:** Cross-cutting concern but doesn't modify business logic, only wraps responses.

### Agent 4: Test Coverage Improvements (Task #10)
**Difficulty:** Easy  
**Work on:** `worktree-agent4`

**Scope:**
- Add 400/404 scenario tests
- Add edge case tests
- Improve test coverage metrics

**Why independent:** Only adds tests, no implementation changes.

## Coordination Strategy

### Git Worktree Setup

```bash
cd /Users/willy/cs146s/modern-software-dev-assignments/week5

# Create worktrees for each agent
git worktree add ../week5-agent1 -b agent1/notes-crud
git worktree add ../week5-agent2 -b agent2/action-items-filter
git worktree add ../week5-agent3 -b agent3/error-handling
git worktree add ../week5-agent4 -b agent4/test-coverage
```

### Warp Tab Organization

**Tab 1 (Agent 1):** `cd ../week5-agent1`
- Autonomy: Medium (require confirmation for file edits)
- Focus: Notes CRUD

**Tab 2 (Agent 2):** `cd ../week5-agent2`
- Autonomy: Medium (require confirmation for file edits)
- Focus: Action items filtering

**Tab 3 (Agent 3):** `cd ../week5-agent3`
- Autonomy: High (error handling is well-scoped)
- Focus: Global error handlers

**Tab 4 (Agent 4):** `cd ../week5-agent4`
- Autonomy: High (tests are safe to auto-generate)
- Focus: Test coverage

### File Conflict Prevention

| Agent | Modified Files | Potential Conflicts |
|-------|---------------|---------------------|
| Agent 1 | `routers/notes.py`, `schemas.py`, `tests/test_notes.py` | Low (isolated to notes) |
| Agent 2 | `routers/action_items.py`, `schemas.py`, `tests/test_action_items.py` | Low (isolated to action_items) |
| Agent 3 | `main.py` (exception handlers), all test files | Medium (touches main.py) |
| Agent 4 | All test files | Medium (overlaps with other test additions) |

**Conflict Resolution Plan:**
1. Agent 3 completes first (foundational error handling)
2. Agents 1 & 2 run concurrently (no overlap)
3. Agent 4 runs last (incorporates all changes for comprehensive tests)

### Communication Protocol

**Checkpoints:**
- Each agent reports completion status
- Merge order: Agent 3 → Agent 1 → Agent 2 → Agent 4
- Run full test suite after each merge

## Agent Prompts

### Agent 1 Prompt (Notes CRUD)
```
Navigate to /Users/willy/cs146s/modern-software-dev-assignments/week5-agent1

Implement full CRUD for notes:
1. Add PUT /notes/{id} endpoint in routers/notes.py
2. Add DELETE /notes/{id} endpoint
3. Add NoteUpdate schema in schemas.py with validation
4. Add tests in tests/test_notes.py for:
   - Successful update
   - Update non-existent note (404)
   - Invalid update data (422)
   - Successful delete
   - Delete non-existent note (404)

Use these validation rules:
- content: min_length=1, max_length=5000
- created_at: read-only

Run tests after implementation: make test
```

### Agent 2 Prompt (Action Items Filter)
```
Navigate to /Users/willy/cs146s/modern-software-dev-assignments/week5-agent2

Add filtering to action items:
1. Update GET /action-items in routers/action_items.py
2. Add query parameter: completed: Optional[bool] = None
3. Filter SQLAlchemy query based on completed status
4. Add tests in tests/test_action_items.py for:
   - Filter completed=true (only completed items)
   - Filter completed=false (only incomplete items)
   - No filter (all items)
   - Empty results

Run tests after implementation: make test
```

### Agent 3 Prompt (Error Handling)
```
Navigate to /Users/willy/cs146s/modern-software-dev-assignments/week5-agent3

Implement global error handling:
1. In main.py, add exception handlers:
   - HTTPException → {"ok": false, "error": {"code": "...", "message": "..."}}
   - ValidationError → {"ok": false, "error": {"code": "VALIDATION_ERROR", ...}}
   - General Exception → {"ok": false, "error": {"code": "INTERNAL_ERROR", ...}}

2. Wrap successful responses: {"ok": true, "data": ...}

3. Update schemas.py with validation:
   - Add min_length constraints
   - Add Field validators

4. Update all tests to check envelope structure

Run tests after implementation: make test
```

### Agent 4 Prompt (Test Coverage)
```
Navigate to /Users/willy/cs146s/modern-software-dev-assignments/week5-agent4

Improve test coverage:
1. Run coverage analysis: PYTHONPATH=. pytest backend/tests --cov=backend/app --cov-report=term-missing

2. Add missing tests for 400/404 scenarios:
   - Invalid request bodies
   - Missing required fields
   - Non-existent resource IDs

3. Add edge case tests:
   - Empty string inputs
   - Very long inputs
   - Special characters

4. Aim for >90% coverage

Run tests after implementation: make test
```

## Supervision Strategy

### Monitoring Points

1. **Before starting:** Review each agent's plan
2. **During execution:** Check for unexpected file modifications
3. **After completion:** Validate tests pass in each worktree
4. **Before merge:** Review diffs for conflicts

### Rollback Plan

If agent causes issues:
```bash
# In specific worktree
git reset --hard HEAD
git clean -fd

# Or abandon worktree
cd /Users/willy/cs146s/modern-software-dev-assignments/week5
git worktree remove ../week5-agentN
git branch -D agentN/task-name
```

## Success Metrics

- ✅ All 4 agents complete without clobbering each other
- ✅ Each worktree passes tests independently
- ✅ Successful merge of all branches
- ✅ Final test suite passes (make test)
- ✅ Code quality maintained (make lint)
- ✅ Coverage improves overall

## Timeline

**Phase 1: Setup (5 min)**
- Create worktrees
- Open Warp tabs
- Configure agent permissions

**Phase 2: Execution (30-45 min)**
- Start Agent 3 (foundational)
- Wait for Agent 3 completion
- Start Agents 1 & 2 concurrently
- Start Agent 4 after others complete

**Phase 3: Integration (15 min)**
- Merge branches in order
- Resolve any conflicts
- Run full test suite
- Validate coverage

**Total estimated time:** 50-65 minutes

## Risk Assessment

| Risk | Severity | Mitigation |
|------|----------|------------|
| File conflicts | High | Use git worktrees |
| Test conflicts | Medium | Agent 4 runs last |
| Schema conflicts | Medium | Careful merge order |
| Main.py conflicts | Medium | Agent 3 completes first |
| Agent confusion | Low | Clear, scoped prompts |

## Post-Execution

After successful completion:
1. Document actual time taken
2. Note any conflicts encountered
3. Measure final test coverage
4. Record lessons learned for writeup.md
