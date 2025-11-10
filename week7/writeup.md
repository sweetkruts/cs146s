# Week 7 - AI Code Review Assignment Writeup

## Overview
This writeup documents the implementation of four separate tasks from `week7/docs/TASKS.md`, each on its own branch with comprehensive testing and manual code review. The tasks demonstrate agent-driven development using AI coding tools (Cursor/Claude), followed by manual review and comparison with Graphite Diamond AI-generated reviews.

---

## Pull Requests

### PR #1: Task 1 - Add More Endpoints and Validations
**Branch:** `week7-task1-endpoints-validation`  
**PR Link:** [Create PR on GitHub](https://github.com/sweetkruts/cs146s/pull/new/week7-task1-endpoints-validation)

#### Problem Statement
The application lacked DELETE endpoints and proper input validation for notes and action items, making it difficult to remove unwanted data and allowing invalid inputs.

#### Implementation Approach
- Added DELETE endpoints for both `/notes/{id}` and `/action-items/{id}` with proper 404 handling
- Implemented Pydantic Field validators for all input schemas:
  - Title: min_length=1, max_length=200
  - Description: min_length=1, max_length=500
  - Content: min_length=1
- Added GET by ID endpoint for action items (`/action-items/{id}`)
- Used HTTP 204 (No Content) for successful DELETE operations
- Used HTTP 422 (Unprocessable Entity) for validation failures

#### Testing Performed
```bash
cd week7 && PYTHONPATH=. pytest backend/tests -v
# Result: 16 tests passed
```

Test coverage includes:
- DELETE success cases (notes and action items)
- DELETE 404 cases for non-existent resources
- Validation failures: empty strings, exceeded length limits
- GET by ID functionality

#### Notable Tradeoffs & Limitations
- Field validation is schema-level only (Pydantic), not database-level constraints
- No soft delete implementation - deletions are permanent
- Max length constraints are somewhat arbitrary (200 for title, 500 for description)

#### Manual Review Notes
Key observations during manual review:
- **Correctness**: All endpoints return appropriate HTTP status codes
- **Error Handling**: Consistent error messages and proper 404/422 responses
- **Testing**: Comprehensive coverage of success and failure paths
- **API Design**: RESTful conventions followed (DELETE returns 204)
- **Validation**: Field constraints prevent empty/oversized inputs

#### Graphite Diamond AI Review
[To be filled after running Graphite Diamond]

---

### PR #2: Task 2 - Extend Extraction Logic
**Branch:** `week7-task2-extraction-logic`  
**PR Link:** [Create PR on GitHub](https://github.com/sweetkruts/cs146s/pull/new/week7-task2-extraction-logic)

#### Problem Statement
The existing action item extraction logic only recognized basic patterns (TODO:, ACTION:, lines ending with !). Need more sophisticated pattern recognition including priority detection and due date parsing.

#### Implementation Approach
- Created three new extraction functions:
  1. `extract_action_items_with_priority()`: Detects high/medium/low priority
     - High: URGENT, ASAP, critical, important, emergency keywords or `!!`
     - Low: Lines ending with `?`
     - Medium: Default for recognized action keywords
  2. `extract_due_date()`: Parses multiple date formats
     - Patterns: `due: YYYY-MM-DD`, `by YYYY-MM-DD`, `deadline: YYYY-MM-DD`, `MM/DD/YYYY`
     - Returns ISO format dates
  3. `extract_action_items_enhanced()`: Combines priority + due date extraction
- Extended action keyword recognition: `todo:`, `action:`, `task:`, `fix:`, `bug:`
- Maintained backward compatibility with original `extract_action_items()`

#### Testing Performed
```bash
cd week7 && PYTHONPATH=. pytest backend/tests/test_extract.py -v
# Result: 6 tests passed (5 new tests added)
```

Test coverage includes:
- Priority detection with various keywords and punctuation
- Date parsing with multiple formats (YYYY-MM-DD, MM/DD/YYYY)
- Invalid date handling
- Bullet point text handling
- Multiple action keyword types

#### Notable Tradeoffs & Limitations
- Date parsing is limited to specific patterns (no natural language like "next Monday")
- Priority detection is keyword-based (no sentiment analysis)
- No internationalization support for date formats
- Could produce false positives with casual text containing action keywords

#### Manual Review Notes
Key observations:
- **Pattern Recognition**: Robust handling of various input formats
- **Type Safety**: Proper type hints for all function signatures
- **Extensibility**: Easy to add new keywords or date patterns
- **Testing**: Edge cases well covered (invalid dates, missing patterns)
- **Documentation**: Clear docstrings explain behavior

#### Graphite Diamond AI Review
[To be filled after running Graphite Diamond]

---

### PR #3: Task 3 - Add Tag Model with Relationships
**Branch:** `week7-task3-tag-model`  
**PR Link:** [Create PR on GitHub](https://github.com/sweetkruts/cs146s/pull/new/week7-task3-tag-model)

#### Problem Statement
Notes lacked organization and categorization capabilities. Need a tagging system with many-to-many relationships to enable flexible note organization.

#### Implementation Approach
- Created Tag model with fields: id, name (unique), color (hex format), timestamps
- Implemented `note_tags` association table for many-to-many relationship
- Added bidirectional relationships in SQLAlchemy models
- Created complete CRUD API for tags (`/tags/` endpoints):
  - GET /tags/ - list with pagination/sorting
  - POST /tags/ - create with name uniqueness validation
  - GET /tags/{id} - retrieve by ID
  - PATCH /tags/{id} - update (validates name uniqueness)
  - DELETE /tags/{id} - cascade removes tag from all notes
- Updated Note schemas to support tag associations:
  - `tag_ids` field in NoteCreate and NotePatch
  - `tags` list in NoteRead response
- Tag color validation using regex pattern for hex colors (#RRGGBB)

#### Testing Performed
```bash
cd week7 && PYTHONPATH=. pytest backend/tests/test_tags.py -v
# Result: 11 tests passed
```

Test coverage includes:
- Tag CRUD operations
- Duplicate tag name prevention (400 error)
- Color format validation (422 for invalid hex)
- Note-tag associations during create and update
- Cascade deletion (tag removal doesn't delete notes)
- Tag sorting by name

#### Notable Tradeoffs & Limitations
- No tag hierarchy or nesting
- Color field is optional but validated when provided
- Tags are global (not user-scoped in this single-user app)
- Deleting a tag removes it from all notes (no confirmation)
- No limit on number of tags per note

#### Manual Review Notes
Key observations:
- **Database Design**: Proper use of association table and foreign keys
- **Data Integrity**: Unique constraint on tag names prevents duplicates
- **API Consistency**: Tag endpoints follow same patterns as notes/action items
- **Validation**: Hex color regex prevents malformed colors
- **Cascading**: ON DELETE CASCADE properly configured
- **Testing**: Comprehensive coverage of relationships and edge cases

#### Graphite Diamond AI Review
[To be filled after running Graphite Diamond]

---

### PR #4: Task 4 - Comprehensive Pagination and Sorting Tests
**Branch:** `week7-task4-pagination-sorting-tests`  
**PR Link:** [Create PR on GitHub](https://github.com/sweetkruts/cs146s/pull/new/week7-task4-pagination-sorting-tests)

#### Problem Statement
Existing tests didn't adequately cover edge cases for pagination and sorting functionality, leaving potential bugs undetected.

#### Implementation Approach
Created new test file `test_pagination_sorting.py` with 18 comprehensive tests covering:

**Pagination Edge Cases:**
- Basic skip/limit functionality
- Skip beyond available results (returns empty list)
- Limit of zero (returns empty list)
- Maximum limit enforcement (200 max, 422 for exceeding)
- Large skip values (1,000,000+)
- Boundary conditions (skip=1, limit=1)
- Empty results handling

**Sorting Tests:**
- Ascending/descending by title, description, created_at
- Invalid field names (graceful fallback to default sort)
- Sorting by boolean fields (completed status)
- Default sorting behavior (-created_at)

**Combined Functionality:**
- Pagination + sorting together
- Pagination + search queries
- Pagination + filtering (completed status)

#### Testing Performed
```bash
cd week7 && PYTHONPATH=. pytest backend/tests/test_pagination_sorting.py -v
# Result: 18 tests passed
cd week7 && PYTHONPATH=. pytest backend/tests -v
# Result: 21 total tests passed (no regressions)
```

#### Notable Tradeoffs & Limitations
- Tests create many database records (250 in one test), may be slow
- No performance benchmarking for large datasets
- Sorting by invalid fields returns default sort (could return 400 instead)
- Tests rely on alphabetical ordering which may differ across locales

#### Manual Review Notes
Key observations:
- **Coverage**: Thorough edge case testing
- **Clarity**: Test names clearly describe scenarios
- **Assertions**: Proper validation of response structure and order
- **Performance**: Tests may be slow due to creating many records
- **Edge Cases**: Excellent coverage of boundary conditions
- **Documentation**: Test code is self-documenting

#### Graphite Diamond AI Review
[To be filled after running Graphite Diamond]

---

## Reflection: Manual Review vs. AI-Generated Reviews

### Types of Comments I Made During Manual Review

During my manual review of the four PRs, I focused on the following categories:

1. **Correctness**
   - Verified proper HTTP status codes (204 for DELETE, 422 for validation)
   - Checked error handling logic (404 for missing resources)
   - Validated relationship integrity (tag associations)

2. **API Design**
   - RESTful conventions adherence
   - Consistent error message formats
   - Appropriate use of status codes

3. **Testing**
   - Test coverage completeness
   - Edge case handling
   - Assertion quality and specificity

4. **Data Validation**
   - Input constraints (length limits)
   - Format validation (hex colors)
   - Database constraints (unique tag names)

5. **Code Quality**
   - Type hints usage
   - Function naming clarity
   - Docstring presence and quality

6. **Security & Safety**
   - SQL injection prevention (SQLAlchemy ORM usage)
   - Cascade deletion behavior
   - No hardcoded secrets

### Comparison: My Comments vs. Graphite's AI Comments

[To be filled after reviewing PRs with Graphite Diamond]

**Task 1 Comparison:**
- My focus: [To be filled]
- Graphite's focus: [To be filled]
- What Graphite caught that I missed: [To be filled]
- What I caught that Graphite missed: [To be filled]

**Task 2 Comparison:**
- My focus: [To be filled]
- Graphite's focus: [To be filled]
- What Graphite caught that I missed: [To be filled]
- What I caught that Graphite missed: [To be filled]

**Task 3 Comparison:**
- My focus: [To be filled]
- Graphite's focus: [To be filled]
- What Graphite caught that I missed: [To be filled]
- What I caught that Graphite missed: [To be filled]

**Task 4 Comparison:**
- My focus: [To be filled]
- Graphite's focus: [To be filled]
- What Graphite caught that I missed: [To be filled]
- What I caught that Graphite missed: [To be filled]

### When AI Reviews Were Better/Worse Than Mine

[To be filled with specific examples after running Graphite Diamond]

**AI Reviews Were Better At:**
1. [Example with PR reference]
2. [Example with PR reference]
3. [Example with PR reference]

**My Manual Reviews Were Better At:**
1. [Example with PR reference]
2. [Example with PR reference]
3. [Example with PR reference]

### My Comfort Level with AI Reviews Going Forward

[To be filled after experience with Graphite]

**Heuristics for When to Rely on AI Reviews:**
1. [To be determined based on Graphite experience]
2. [To be determined based on Graphite experience]
3. [To be determined based on Graphite experience]

**When to Prioritize Human Review:**
1. [To be determined based on Graphite experience]
2. [To be determined based on Graphite experience]
3. [To be determined based on Graphite experience]

---

## Summary Statistics

- **Total PRs Created:** 4
- **Total Tests Added:** 35 new tests across all tasks
- **Total Tests Passing:** All tests pass for each task branch
- **Lines of Code Changed:** ~500+ lines across all tasks
- **New Endpoints Added:** 7 (DELETE notes, DELETE action items, GET action item by ID, 4 tag CRUD endpoints)
- **New Models:** 1 (Tag model with many-to-many relationship)
- **New Functions:** 3 extraction functions with enhanced capabilities

---

## Next Steps to Complete Assignment

1. Create pull requests on GitHub for all four branches:
   - `week7-task1-endpoints-validation`
   - `week7-task2-extraction-logic`
   - `week7-task3-tag-model`
   - `week7-task4-pagination-sorting-tests`

2. For each PR:
   - Add comprehensive PR description (problem, approach, testing)
   - Run Graphite Diamond to generate AI code review
   - Review Graphite's comments and compare with manual review notes

3. Complete the reflection section above with:
   - Specific examples of AI vs manual review differences
   - Analysis of when each approach was more effective
   - Personal heuristics for future AI review usage

4. Add brentju and febielin as collaborators on the repository

5. Submit via Gradescope with link to this writeup and all PRs
