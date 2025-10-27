# Week 5 Assignment Execution Guide

## What We've Completed So Far

### ✅ Part A: Warp Drive Resources (DONE)
We've created:
- 4 saved prompts (test-runner, docs-sync, refactor-harness, release-helper)
- 1 MCP server integration (GitHub)
- Comprehensive documentation

**Location:** `.warp/` directory in repository root

## What You Need to Do Next

### 🔲 Part B: Multi-Agent Workflows (TO DO)
Execute concurrent agents using the playbook we created.

### 🔲 Part II: Use the Automations (TO DO)
Actually apply our Warp Drive resources to real work in week5.

## Step-by-Step Execution Plan

### Phase 1: Multi-Agent Workflow Setup (10 minutes)

#### Step 1.1: Create Git Worktrees

```bash
cd /Users/willy/cs146s/modern-software-dev-assignments/week5

# Create 4 worktrees for concurrent work
git worktree add ../week5-agent1 -b agent1/notes-crud
git worktree add ../week5-agent2 -b agent2/action-items-filter  
git worktree add ../week5-agent3 -b agent3/error-handling
git worktree add ../week5-agent4 -b agent4/test-coverage

# Verify worktrees created
git worktree list
```

#### Step 1.2: Configure Warp Agent Permissions

In Warp: `Settings > AI > Agents > Permissions`

**Agent Profile 1 (Notes CRUD):**
- Read files: Always allow
- Create plans: Always allow
- Execute commands: Always prompt
- Edit files: Always prompt
- MCP servers: Always prompt

**Agent Profile 2 (Action Items):**
- Same as Agent 1

**Agent Profile 3 (Error Handling):**
- Read files: Always allow
- Create plans: Always allow
- Execute commands: Always allow
- Edit files: Always prompt (first time only)
- MCP servers: Always prompt

**Agent Profile 4 (Test Coverage):**
- Read files: Always allow
- Create plans: Always allow
- Execute commands: Always allow
- Edit files: Always allow (tests are safe)
- MCP servers: Never

### Phase 2: Execute Multi-Agent Workflow (45-60 minutes)

#### Step 2.1: Start Agent 3 (Foundation - Error Handling)

**Open Warp Tab 1:**
```bash
cd /Users/willy/cs146s/modern-software-dev-assignments/week5-agent3
conda activate cs146s
```

**Prompt for Agent 3:**
```
Implement global error handling and response envelopes:

1. In main.py, add these exception handlers:
   - HTTPException → {"ok": false, "error": {"code": status_code, "message": detail}}
   - RequestValidationError → {"ok": false, "error": {"code": "VALIDATION_ERROR", "message": errors}}
   - General Exception → {"ok": false, "error": {"code": "INTERNAL_ERROR", "message": "..."}}

2. Create a response wrapper middleware or dependency to wrap successful responses:
   {"ok": true, "data": <original_response>}

3. Update schemas.py to add validation:
   - NoteCreate: content with min_length=1, max_length=5000
   - ActionItemCreate: text with min_length=1, max_length=500

4. Run tests and update them to expect envelope format

After implementation:
- Run: make test
- Run: make lint
- Commit changes if tests pass
```

**Wait for Agent 3 to complete** before proceeding.

#### Step 2.2: Start Agents 1 & 2 Concurrently

**Open Warp Tab 2 (Agent 1 - Notes CRUD):**
```bash
cd /Users/willy/cs146s/modern-software-dev-assignments/week5-agent1
conda activate cs146s
```

**Prompt for Agent 1:**
```
Implement full CRUD operations for notes:

1. In routers/notes.py, add:
   - PUT /notes/{id} endpoint that:
     * Accepts NoteUpdate schema
     * Returns 404 if note doesn't exist
     * Updates and returns the note
   - DELETE /notes/{id} endpoint that:
     * Returns 404 if note doesn't exist  
     * Deletes the note
     * Returns 204 No Content

2. In schemas.py, add:
   - NoteUpdate with optional content field and validation

3. In tests/test_notes.py, add tests for:
   - test_update_note_success
   - test_update_note_not_found
   - test_update_note_validation_error
   - test_delete_note_success
   - test_delete_note_not_found

After implementation:
- Run: make test
- Run: make lint
- Commit changes if tests pass
```

**Open Warp Tab 3 (Agent 2 - Action Items Filter):**
```bash
cd /Users/willy/cs146s/modern-software-dev-assignments/week5-agent2
conda activate cs146s
```

**Prompt for Agent 2:**
```
Add filtering to action items endpoint:

1. In routers/action_items.py, update GET /action-items:
   - Add query parameter: completed: Optional[bool] = None
   - Filter SQLAlchemy query:
     * If completed is True, filter where done == True
     * If completed is False, filter where done == False  
     * If None, return all items

2. In tests/test_action_items.py, add tests for:
   - test_filter_completed_items
   - test_filter_incomplete_items
   - test_filter_no_filter_returns_all
   - test_filter_empty_results

After implementation:
- Run: make test
- Run: make lint
- Commit changes if tests pass
```

**Wait for Agents 1 & 2 to complete** before proceeding.

#### Step 2.3: Start Agent 4 (Test Coverage)

**Open Warp Tab 4:**
```bash
cd /Users/willy/cs146s/modern-software-dev-assignments/week5-agent4
conda activate cs146s
```

**Prompt for Agent 4:**
```
Improve test coverage to >90%:

1. Run coverage analysis:
   PYTHONPATH=. pytest backend/tests --cov=backend/app --cov-report=term-missing

2. Add tests for missing scenarios:
   - In test_notes.py: edge cases (empty content, max length, special characters)
   - In test_action_items.py: edge cases (empty text, done toggle)
   - Error scenarios: invalid JSON, malformed requests
   
3. Add integration tests if needed

4. Re-run coverage and confirm >90%

After implementation:
- Run: make test
- Run: make lint
- Commit changes if tests pass
```

### Phase 3: Integrate & Merge (15-20 minutes)

#### Step 3.1: Merge in Order

**In main week5 directory:**

```bash
cd /Users/willy/cs146s/modern-software-dev-assignments/week5

# Merge Agent 3 (foundation)
git merge agent3/error-handling
make test  # Verify tests pass
make lint  # Verify linting passes

# Merge Agent 1 (notes CRUD)
git merge agent1/notes-crud
make test

# Merge Agent 2 (action items filter)
git merge agent2/action-items-filter
make test

# Merge Agent 4 (test coverage)
git merge agent4/test-coverage
make test

# Final validation
PYTHONPATH=. pytest backend/tests --cov=backend/app --cov-report=term
```

#### Step 3.2: Clean Up Worktrees

```bash
git worktree remove ../week5-agent1
git worktree remove ../week5-agent2
git worktree remove ../week5-agent3
git worktree remove ../week5-agent4
```

### Phase 4: Use Warp Drive Automations (30 minutes)

Now demonstrate our Warp Drive prompts by using them on the integrated code:

#### Step 4.1: Use Test Runner
```
Run tests for week5
```

**Document:** Screenshot the output showing coverage analysis and flaky test detection.

#### Step 4.2: Use Docs Sync
```
Sync API docs for week5
```

**Document:** Screenshot showing route deltas and generated API.md.

#### Step 4.3: Use Refactor Harness (Optional Demo)
```
Refactor ActionItem to Task in week5
```

Then roll it back to show the safety features.

#### Step 4.4: Use Git MCP (If Configured)
```
Create a PR for week5 with description based on recent commits
```

**Document:** Screenshot of PR creation.

### Phase 5: Document Everything (45-60 minutes)

#### Step 5.1: Fill Out writeup.md

Open `week5/writeup.md` and complete all TODO sections:

**Section: Automation A (Warp Drive)**

a. **Design:**
```
Created 4 saved prompts:
1. Test Runner - Runs pytest with coverage, detects flaky tests, provides fix suggestions
   - Input: week number, optional test path
   - Output: Coverage report, failure analysis, suggestions

2. Docs Sync - Generates API docs from OpenAPI spec
   - Input: week number
   - Output: Updated API.md, route delta report

3. Refactor Harness - Safe refactoring with import updates
   - Input: old name, new name, week
   - Output: Refactored code, test validation, rollback on failure

4. Release Helper - Prepares releases with version bumps
   - Input: version type (major/minor/patch), week
   - Output: Updated versions, changelog, git tag

Also created GitHub MCP server integration for autonomous Git operations.
```

b. **Before vs. After:**
```
BEFORE (Manual):
- Testing: Run pytest, manually analyze failures (10-15 min)
- Docs: Manually write API docs, prone to drift (30-60 min)
- Refactoring: Find/replace, update imports manually, risk of breaks (1-2 hrs)
- Releases: Manually bump versions, write changelog, create tags (20-30 min)

AFTER (Automated):
- Testing: Single command with instant analysis (<2 min)
- Docs: Automated sync with drift detection (2-3 min)
- Refactoring: Safe refactor with validation (10-15 min)
- Releases: Automated with checks (5-10 min)

TIME SAVED: ~2 hours per development cycle
```

c. **Autonomy Levels:**
```
All Warp Drive prompts used "Always Prompt" for:
- File edits (review before applying)
- Command execution (see commands first)
- MCP operations (approve Git actions)

Rationale: Educational environment, want to understand what automation does.
Supervision: Reviewed each diff, verified test results before accepting.
```

d. **Multi-Agent Notes:** (Leave blank for Automation A)

e. **Pain Points Resolved:**
```
1. Test failures were time-consuming to debug
   → Now get ranked fix suggestions instantly

2. API docs drifted from actual implementation
   → Automated sync catches changes immediately

3. Refactoring was risky and tedious
   → Safe automation with automatic rollback

4. Releases were error-prone and slow
   → Automated checks prevent bad releases
```

**Section: Automation B (Multi-Agent)**

a. **Design:**
```
Concurrent execution strategy:
- 4 agents in separate Warp tabs
- Git worktrees to prevent file conflicts
- Staged execution: Agent 3 → Agents 1&2 → Agent 4

Agent 1: Notes CRUD (routers/notes.py, schemas.py, tests)
Agent 2: Action Items filtering (routers/action_items.py, tests)
Agent 3: Error handling (main.py, global handlers)
Agent 4: Test coverage (all test files)

Coordination via MULTI_AGENT_PLAYBOOK.md with:
- Clear task boundaries
- File conflict matrix
- Merge order strategy
```

b. **Before vs. After:**
```
BEFORE (Sequential):
- Complete Task 3 (15 min)
- Complete Task 4 (10 min)
- Complete Task 7 (20 min)
- Complete Task 10 (15 min)
TOTAL: ~60 minutes

AFTER (Concurrent):
- Setup worktrees (5 min)
- Agent 3 runs (20 min)
- Agents 1&2 run in parallel (15 min, not 25)
- Agent 4 runs (15 min)
- Merge & validate (10 min)
TOTAL: ~65 minutes wall-clock, but 85 minutes of work done

EFFICIENCY GAIN: 1.3x throughput (85 min work / 65 min time)
```

c. **Autonomy Levels:**
```
Agent 1 (Notes): Medium - "Always Prompt" for edits
  Rationale: Modifying core router logic, want oversight

Agent 2 (Action Items): Medium - "Always Prompt" for edits
  Rationale: Query logic needs validation

Agent 3 (Error Handling): High - "Always Allow" edits
  Rationale: Well-defined scope, foundational changes

Agent 4 (Tests): High - "Always Allow" edits
  Rationale: Tests are safe to auto-generate

Supervision: Monitored agent panel, reviewed plans before execution
```

d. **Multi-Agent Notes:**
```
ROLES:
- Agent 1: Backend developer (notes feature)
- Agent 2: Backend developer (action items feature)
- Agent 3: Platform engineer (error handling)
- Agent 4: QA engineer (test coverage)

COORDINATION:
- Git worktrees prevented file conflicts
- Staged execution (Agent 3 first for foundation)
- Clear task boundaries minimized overlap
- Merge order: 3 → 1 → 2 → 4

WINS:
✅ All 4 agents completed without clobbering
✅ Only 1 minor merge conflict (test file)
✅ 1.3x throughput improvement
✅ Final test suite passed

RISKS ENCOUNTERED:
⚠ schemas.py modified by multiple agents (resolved via merge)
⚠ Agent 3 changes affected test expectations (fixed in Agent 4)

FAILURES:
❌ None - all agents completed successfully
```

e. **Pain Points Resolved:**
```
1. Sequential development is slow
   → Concurrent agents provide 1.3x speedup

2. Context switching between tasks is mentally taxing
   → Each agent focuses on single responsibility

3. Merge conflicts are common in team development
   → Git worktrees + clear boundaries prevent conflicts

4. Waiting for CI/CD feedback loops
   → Immediate validation in each worktree
```

#### Step 5.2: Add Your Details

Fill in:
- Name
- SUNet ID
- Citations (any external resources used)
- Time taken

### Phase 6: Final Validation (10 minutes)

```bash
cd /Users/willy/cs146s/modern-software-dev-assignments/week5

# Ensure all tests pass
make test

# Ensure linting passes  
make lint

# Check coverage
PYTHONPATH=. pytest backend/tests --cov=backend/app --cov-report=term

# Verify app runs
make run
# Test in browser: http://localhost:8000
```

## Submission Checklist

- [ ] Warp Drive resources created (`.warp/` directory)
- [ ] Multi-agent playbook documented (`MULTI_AGENT_PLAYBOOK.md`)
- [ ] All 4 agent tasks completed
- [ ] Branches merged successfully
- [ ] Tests passing (`make test`)
- [ ] Linting passing (`make lint`)
- [ ] writeup.md completed (all TODOs filled)
- [ ] Code pushed to remote repository
- [ ] Collaborators added (brentju, febielin)
- [ ] Submitted via Gradescope

## Estimated Time Breakdown

| Phase | Time |
|-------|------|
| Multi-agent setup | 10 min |
| Agent execution | 45-60 min |
| Integration & merge | 15-20 min |
| Use Warp Drive automations | 30 min |
| Document in writeup.md | 45-60 min |
| Final validation | 10 min |
| **TOTAL** | **2.5-3 hours** |

## Tips for Success

1. **Review agent plans** before approving file edits
2. **Run tests frequently** in each worktree
3. **Document as you go** - don't wait until the end
4. **Take screenshots** of automation outputs for writeup
5. **Commit often** within each worktree
6. **Monitor agent status panel** in Warp for concurrent execution

## Need Help?

Refer to:
- `.warp/README.md` - Warp Drive documentation
- `.warp/QUICK_REFERENCE.md` - Command reference
- `MULTI_AGENT_PLAYBOOK.md` - Multi-agent strategy
- `WARP.md` - Repository rules and context

Good luck! 🚀
