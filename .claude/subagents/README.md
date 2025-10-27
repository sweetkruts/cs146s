# SubAgents Documentation

This directory contains configuration and guidelines for specialized AI agents (SubAgents) that work together to manage different aspects of the development workflow.

## Available SubAgents

### 1. TestAgent (`test-agent.md`)
**Specialization**: Testing and test coverage
- Writes comprehensive test cases (TDD approach)
- Ensures high code coverage
- Identifies edge cases
- Verifies implementations meet requirements

### 2. CodeAgent (`code-agent.md`)
**Specialization**: Feature implementation
- Implements features to pass tests
- Follows code standards and patterns
- Maintains code quality
- Handles error cases properly

### 3. DocsAgent (`docs-agent.md`)
**Specialization**: Documentation maintenance
- Keeps API docs in sync with code
- Detects documentation drift
- Maintains task lists
- Ensures comprehensive documentation

## How to Use SubAgents

### Individual Agent Mode
When you need specialized help, invoke an agent by referencing its role:

```
"Acting as TestAgent, write comprehensive tests for the update note endpoint."
```

```
"As CodeAgent, implement the DELETE /notes/{id} endpoint to pass the failing tests."
```

```
"As DocsAgent, update the API documentation to reflect the new search functionality."
```

### Collaborative Workflow

#### Scenario 1: Adding a New Feature
1. **TestAgent** writes failing tests
2. **CodeAgent** implements feature to pass tests
3. **TestAgent** verifies tests pass and coverage is adequate
4. **DocsAgent** updates API documentation and TASKS.md

Example conversation:
```
User: "Add a DELETE endpoint for notes"

TestAgent: [Writes tests for DELETE /notes/{id}]
CodeAgent: [Implements the delete functionality]
TestAgent: [Verifies tests pass, checks coverage]
DocsAgent: [Updates API.md with DELETE endpoint docs]
```

#### Scenario 2: Bug Fix
1. **TestAgent** writes failing test reproducing the bug
2. **CodeAgent** fixes the bug to make test pass
3. **TestAgent** verifies fix and adds regression tests
4. **DocsAgent** updates docs if behavior changed

#### Scenario 3: Documentation Review
1. **DocsAgent** compares OpenAPI spec with docs
2. **DocsAgent** identifies missing/outdated documentation
3. **CodeAgent** verifies endpoints work as documented
4. **TestAgent** adds tests for undocumented behavior
5. **DocsAgent** updates documentation

## Agent Communication Protocol

### TestAgent → CodeAgent
```
Tests written for [feature]:
- test_[name]: expects [behavior]
- test_[name]: expects [error handling]

All tests failing as expected (TDD).
Ready for implementation.
```

### CodeAgent → TestAgent
```
Implementation complete for [feature].
Files modified: [list]

Please verify:
- Tests pass
- No regressions
- Coverage adequate
```

### CodeAgent → DocsAgent
```
Endpoints added/modified:
- [METHOD] /path: [description]

Schema changes:
- [details]

Ready for documentation update.
```

### DocsAgent → CodeAgent
```
Documentation drift detected:
- Undocumented: [endpoint]
- Schema mismatch: [details]

Please clarify or implement.
```

## Best Practices

### Context Sharing
- Reference previous agent outputs explicitly
- Include relevant file paths and line numbers
- Share test results or error messages
- Provide clear handoff points

### Agent Specialization
- Don't ask TestAgent to write production code
- Don't ask CodeAgent to write test cases
- Don't ask DocsAgent to implement features
- Stay within agent expertise boundaries

### Workflow Efficiency
- Run agents in parallel for independent tasks:
  - TestAgent writing tests for feature A
  - CodeAgent implementing feature B (tests already exist)
  - DocsAgent updating docs for completed feature C
- Use sequential flow when tasks depend on each other
- Clear context (`/clear`) when switching between unrelated features

### Quality Gates
Each agent should verify their work:
- **TestAgent**: All tests pass, coverage >80%
- **CodeAgent**: Tests pass, linting clean, type hints complete
- **DocsAgent**: All endpoints documented, no drift detected

## Example Multi-Agent Session

```
User: "Add search functionality to action items"

[TestAgent activates]
TestAgent: Writing tests for GET /action-items/search?q=...
Created tests:
- test_search_action_items_by_description
- test_search_action_items_empty_query
- test_search_action_items_no_results

All tests fail as expected. Ready for CodeAgent.

[CodeAgent activates]
CodeAgent: Implementing search endpoint in routers/action_items.py
Added endpoint with SQLAlchemy filters.
Running tests... All pass!
Formatted and linted. Ready for TestAgent verification.

[TestAgent activates]
TestAgent: Verified implementation.
✓ All tests pass
✓ Coverage: 92%
✓ No regressions
Implementation approved. Ready for DocsAgent.

[DocsAgent activates]
DocsAgent: Updated API.md with search endpoint documentation.
Added examples and error codes.
No drift detected. Documentation complete.

[Summary]
✅ Feature complete: Search action items
✅ Tests: 3 new tests, all passing
✅ Coverage: 92%
✅ Documentation: Updated
```

## Integration with Custom Commands

SubAgents work seamlessly with custom slash commands:

- `/test-suite` - Run by TestAgent to verify implementation
- `/docs-sync` - Run by DocsAgent to update documentation
- `/add-endpoint` - Coordinates all three agents in TDD workflow

## Tips for Effective Agent Usage

1. **Be explicit about which agent should act**
2. **Provide clear success criteria**
3. **Share context between agents**
4. **Use agents iteratively** (don't try to do everything at once)
5. **Verify each step** before moving to next agent
6. **Document agent decisions** in commits or comments

## Customization

To customize agent behavior:
1. Edit the respective `.md` file
2. Adjust responsibilities, standards, or workflows
3. Add project-specific guidelines
4. Update communication protocols if needed

## Troubleshooting

### Agent Overlap
If agents step on each other's toes:
- Clarify boundaries in agent files
- Use explicit agent invocation
- Run agents sequentially rather than in parallel

### Context Loss
If agents lose context:
- Provide explicit handoffs with file paths and details
- Reference previous outputs
- Use `/clear` to reset when starting new feature

### Quality Issues
If output quality decreases:
- Review agent checklist completion
- Verify quality gates are enforced
- Add more specific standards to agent files


