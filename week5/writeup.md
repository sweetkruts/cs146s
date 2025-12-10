# Week 5 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: William Li \
SUNet ID: willyli \
Citations:
- [Warp Documentation](https://docs.warp.dev/)
- [Warp University](https://www.warp.dev/university)
- [Git Worktree Documentation](https://git-scm.com/docs/git-worktree)

This assignment took me about **1** hours to do. 


## YOUR RESPONSES
### Automation A: Warp Drive saved prompts, rules, MCP servers

a. Design of each automation, including goals, inputs/outputs, steps
> Created 4 saved prompts in `.warp/prompts/` and 1 MCP server integration:
>
> **1. Test Runner (`test-runner.md`)**
> - Goal: Run tests with coverage analysis, flaky test detection, and actionable feedback
> - Inputs: Week directory, optional test path
> - Outputs: Test results, coverage report, failure analysis with fix suggestions
> - Steps: Navigate to directory, run pytest with fail-fast, analyze results, detect flaky tests, run coverage if passing, provide ranked fix suggestions
>
> **2. Docs Sync (`docs-sync.md`)**
> - Goal: Generate/update API documentation from OpenAPI spec and detect route deltas
> - Inputs: Week directory
> - Outputs: Updated API.md, route delta report (new/modified/removed endpoints), documentation coverage percentage
> - Steps: Start server, fetch OpenAPI spec, parse existing docs, compare and identify changes, generate comprehensive API.md, report deltas
>
> **3. Refactor Harness (`refactor-harness.md`)**
> - Goal: Safe refactoring with automatic import updates and rollback on failure
> - Inputs: Old name, new name, week directory
> - Outputs: Refactored code, updated imports, test validation results, backup branch created
> - Steps: Preview affected files, create backup branch, update all imports and references, run linter, run test suite, rollback on failure
>
> **4. Release Helper (`release-helper.md`)**
> - Goal: Prepare releases with version bumps, checks, changelog generation, and tagging
> - Inputs: Version type (major/minor/patch), week directory
> - Outputs: Version updates, changelog, git tag, push instructions
> - Steps: Validate clean tree, determine version, run tests/linting/coverage, generate changelog from commits, update version files, create commit and tag
>
> **5. GitHub MCP Server (`.warp/mcp/`)**
> - Goal: Enable autonomous Git operations (branches, commits, PRs, tags)
> - Integration: Docker-based MCP server with GitHub API
> - Configuration: Stored in `git-mcp-config.json` with token authentication
> - Capabilities: Create branches, commit changes, manage PRs, create tags, query repo status

b. Before vs. after (i.e. manual workflow vs. automated workflow)
> **Before (Manual):**
> - Testing: Run pytest, manually parse verbose output, identify failures, run coverage separately, analyze coverage report which is slow
> - Docs: Manually write API docs by reading code, compare with Swagger UI, prone to drift and staleness 
> - Refactoring: Find/replace across files, manually update imports, risk of breaking code, no automatic rollback (1-2 hours per refactor)
> - Releases: Manually bump versions in multiple files, write changelog, create tag, validate tests (20-30 min, error-prone)
>
> **After (Automated):**
> - Testing: Single command `Run tests for week5`, instant analysis with ranked fixes (<2 min)
> - Docs: Single command `Sync API docs for week5`, automated drift detection (2-3 min)
> - Refactoring: Single command `Refactor X to Y in week5`, safe with rollback (10-15 min)
> - Releases: Single command `Prepare release minor for week5`, automated checks (5-10 min)

c. Autonomy levels used for each completed task (what code permissions, why, and how you supervised)
> All Warp Drive prompts configured with **"Always Prompt"** for:
> - File edits: Review changes before applying
> - Command execution: See commands before running
> - MCP operations: Approve Git actions explicitly
>
> **Rationale:**
> Educational environment where understanding automation behavior is important. Supervision ensures:
> - Verification of test results before acceptance
> - Review of documentation changes for accuracy
> - Validation of refactoring scope
> - Control over release process
>
> **Supervision approach:**
> - Reviewed each diff before approving file edits
> - Verified test results matched expectations
> - Checked coverage metrics for reasonableness
> - Confirmed documentation accuracy against implementation
> - Never granted blanket "Always Allow" permissions

d. (if applicable) Multi‑agent notes: roles, coordination strategy, and concurrency wins/risks/failures
> Not applicable for Automation A (Warp Drive prompts).

e. How you used the automation (what pain point it resolves or accelerates)
> **Pain Points Resolved:**
>
> 1. **Test Failure Debugging**
>    - Before: 10-15 minutes to identify root cause, search code, experiment with fixes
>    - After: Test Runner provides ranked fix suggestions instantly
>    - Example: When note update failed, runner identified missing null check and suggested exact fix
>
> 2. **Documentation Drift**
>    - Before: API docs became stale, required manual comparison with code
>    - After: Docs Sync detects drift automatically, generates complete documentation
>    - Example: After adding PUT/DELETE endpoints, docs synced in 2 minutes with full coverage
>
> 3. **Refactoring Risk**
>    - Before: Find/replace broke imports, manual import updates error-prone
>    - After: Refactor Harness updates all imports, validates with tests, rolls back on failure
>    - Example: Would use for renaming ActionItem to Task across codebase safely
>
> 4. **Release Process**
>    - Before: Forgot to run tests, version bumps inconsistent, changelog manual
>    - After: Release Helper enforces quality gates, automates version management
>    - Example: Would ensure no releases without passing tests and proper changelog



### Automation B: Multi‑agent workflows in Warp 

a. Design of each automation, including goals, inputs/outputs, steps
> Implemented 3 self-contained tasks that could be executed by concurrent agents:
>
> **Task #3: Notes CRUD Operations**
> - Goal: Add full CRUD operations (PUT/DELETE) for notes
> - Scope: `routers/notes.py`, `schemas.py`, `tests/test_notes.py`
> - Steps:
>   1. Add NoteUpdate schema with validation (min_length=1, max_length=5000)
>   2. Implement PUT /notes/{id} endpoint with partial update support
>   3. Implement DELETE /notes/{id} endpoint with 204 status
>   4. Add tests for success, not found, and partial update cases
>   5. Run tests and validate
>
> **Task #7: Error Handling & Response Envelopes**
> - Goal: Implement global error handlers and consistent response format
> - Scope: `main.py`, all test files
> - Steps:
>   1. Add exception handlers for HTTPException, ValidationError, general Exception
>   2. Wrap errors in consistent envelope: `{"ok": false, "error": {"code": X, "message": Y}}`
>   3. Add Pydantic Field validation (min_length, max_length) to all schemas
>   4. Update tests to verify envelope structure
>   5. Add tests for validation errors and error responses
>
> **Task #10: Test Coverage Improvements**
> - Goal: Increase test coverage with edge cases and validation tests
> - Scope: All test files
> - Steps:
>   1. Add tests for maximum length inputs (5000 chars for content, 500 for descriptions)
>   2. Add tests for exceeding maximum lengths
>   3. Add tests for special characters in search
>   4. Add tests for empty results
>   5. Add tests for completing already completed items
>   6. Test empty update payloads
>
> **Coordination Strategy:**
> - Tasks designed to minimize file conflicts
> - Task #7 completed first (foundational error handling)
> - Tasks #3 and #10 could run concurrently (different focuses)
> - Used git worktree pattern documented in `MULTI_AGENT_PLAYBOOK.md`

b. Before vs. after (i.e. manual workflow vs. automated workflow)
> **Before (Sequential Development):**
> - Task #3: Write tests, implement endpoints, validate (20 min)
> - Task #7: Add error handlers, update tests, validate (15 min)
> - Task #10: Add edge case tests, run coverage (15 min)
> - Context switching: 3 switches between different concerns
> - there would also be insanely high context switching overhead which is mental strain
>
> **After (Concurrent Multi-Agent):**
> - Setup: Create 3 git worktrees, configure agent tabs 
> - Agent 1 (Task #7): Error handling foundation 
> - Agents 2 & 3 (parallel): CRUD + test coverage 
> - Integration: Merge branches, resolve conflicts (5 min)
>

c. Autonomy levels used for each completed task (what code permissions, why, and how you supervised)
> **Task #3 (Notes CRUD):**
> - Autonomy: Medium
> - Permissions: "Always Prompt" for file edits
> - Rationale: Modifying core router logic, wanted oversight on endpoint implementation
> - Supervision: Reviewed schema design, validated endpoint implementations match REST conventions, confirmed proper status codes (200, 204, 404)
>
> **Task #7 (Error Handling):**
> - Autonomy: High
> - Permissions: "Always Allow" for main.py, "Always Prompt" for tests
> - Rationale: Well-defined scope (exception handlers), foundational infrastructure
> - Supervision: Verified error envelope structure consistent, checked error codes match HTTP standards
>
> **Task #10 (Test Coverage):**
> - Autonomy: High  
> - Permissions: "Always Allow" for test files
> - Rationale: Tests are safe to auto-generate, worst case they fail and get fixed
> - Supervision: Reviewed test assertions for correctness, validated edge cases were meaningful

d. (if applicable) Multi‑agent notes: roles, coordination strategy, and concurrency wins/risks/failures
NA
e. How you used the automation (what pain point it resolves or accelerates)

I think the main pain point solved is that it automates a lot of manual, brain-dead work that is uninteresting but still takes time for the developer. Before, someone might have a bunch of tasks that they have to do sequentially but with warp parallel agents, we can just have different agents go do work and then manage/watch the LLM agent and guide it when necessary. Specifically, agent 1 build error handling and agent 2 can work on CRUD in parallel.

This accelerates the SLDC since people can put their boring and tedious work away to agents in paralell.



