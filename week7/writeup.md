# Week 7 Write-up

## Submission Details

Name: **William Li** \
SUNet ID: **willyli** \
Citations: **Claude (Cursor) for implementation, Graphite Diamond for AI code review**

This assignment took me about **2** hours to do. 


## Task 1: Add more endpoints and validations

### a. Links to relevant commits/issues
- Branch: `week7-task1-endpoints-validation`
- PR: https://app.graphite.com/github/pr/sweetkruts/cs146s/1
- Commit: https://github.com/sweetkruts/cs146s/commit/8d7537a

### b. PR Description
**Problem Statement:**
The application lacked DELETE endpoints and proper input validation for notes and action items, making it difficult to remove unwanted data and allowing invalid inputs.

**Implementation Approach:**
Added DELETE endpoints for both `/notes/{id}` and `/action-items/{id}` with proper 404 handling. Implemented Pydantic Field validators for all input schemas with title max length of 200 chars, description max of 500 chars, and minimum length of 1 for all fields. Also added GET by ID endpoint for action items. Used HTTP 204 for successful deletions and HTTP 422 for validation failures.

**Testing Performed:**
```bash
cd week7 && PYTHONPATH=. pytest backend/tests -v
# Result: 16 tests passed
```

Added 8 new tests covering DELETE success cases, 404 cases for non-existent resources, validation failures for empty strings and exceeded length limits, and GET by ID functionality.

**Notable Tradeoffs:**
Field validation is schema-level only (Pydantic), not database-level. No soft delete implementation, so deletions are permanent. Max length constraints are somewhat arbitrary.

### c. Graphite Diamond generated code review

**DELETE endpoints use db.flush() instead of db.commit()** - Verify this is intentional and works with your transaction management strategy. Typically you'd expect db.commit().

**Validation is asymmetric** - Notes have unlimited content length but action items are capped at 500 chars for description. Confirm this matches your requirements.

**Missing GET endpoint for notes** - You added GET by ID for action items but notes don't have an explicit GET by ID endpoint (only the implicit one in the PATCH route). Consider if notes should also have a dedicated GET endpoint for consistency.

**Test coverage for GET by ID** - The test for GET /notes/{note_id} expects 404 after deletion, but there's no explicit GET endpoint in the notes router. This test might be failing or relying on something else.

**Edge cases** - The validation tests look good, but consider testing the boundary conditions (200 chars exactly, 500 chars exactly).

---

## Task 2: Extend extraction logic

### a. Links to relevant commits/issues
- Branch: `week7-task2-extraction-logic`
- PR: https://app.graphite.com/github/pr/sweetkruts/cs146s/2
- Commit: https://github.com/sweetkruts/cs146s/commit/aca424e

### b. PR Description
**Problem Statement:**
The existing action item extraction logic only recognized basic patterns (TODO:, ACTION:, lines ending with !). Need more sophisticated pattern recognition including priority detection and due date parsing.

**Implementation Approach:**
Created three new extraction functions. First, `extract_action_items_with_priority()` detects high/medium/low priority based on keywords like URGENT, ASAP, critical, important, emergency for high priority, and lines ending with ? for low priority. Second, `extract_due_date()` parses multiple date formats including YYYY-MM-DD and MM/DD/YYYY with keywords like "due:", "by", and "deadline:". Third, `extract_action_items_enhanced()` combines both priority and due date extraction. Extended action keyword recognition to include todo:, action:, task:, fix:, and bug:.

**Testing Performed:**
```bash
cd week7 && PYTHONPATH=. pytest backend/tests/test_extract.py -v
# Result: 6 tests passed
```

Added 5 new tests covering priority detection with various keywords and punctuation, date parsing with multiple formats, invalid date handling, and bullet point text handling.

**Notable Tradeoffs:**
Date parsing is limited to specific patterns with no natural language support. Priority detection is keyword-based without sentiment analysis. No internationalization support for dates or keywords.

### c. Graphite Diamond generated code review

**Priority detection logic** - The conditions in extract_action_items_with_priority and extract_action_items_enhanced check for !! after already checking endswith("!"), which means single ! will match both conditions.

**Code duplication** - The three extraction functions share significant logic. Consider if extract_action_items_with_priority and the base extract_action_items are still needed, or if extract_action_items_enhanced could replace them.

**Date format coverage** - extract_due_date only handles specific formats. Consider if other common formats (e.g., "Nov 15", "15th November") should be supported based on your requirements.

**Silent error handling** - Invalid dates in extract_due_date return None without logging. This might make debugging difficult if users expect dates to be parsed but they're silently skipped.

**Keyword case sensitivity** - The code lowercases text for matching but returns the original text, which is good. Verify this handles all expected input formats.

**Action keyword prefixes** - The logic uses startswith for action keywords but also checks for ! suffix, which could match unintended lines ending with !.

---

## Task 3: Try adding a new model and relationships

### a. Links to relevant commits/issues
- Branch: `week7-task3-tag-model`
- PR: https://app.graphite.com/github/pr/sweetkruts/cs146s/3
- Commit: https://github.com/sweetkruts/cs146s/commit/26fb69f

### b. PR Description
**Problem Statement:**
Notes lacked organization and categorization capabilities. Need a tagging system with many-to-many relationships to enable flexible note organization.

**Implementation Approach:**
Created a Tag model with id, name (unique), color (hex format), and timestamps. Implemented a `note_tags` association table for the many-to-many relationship between notes and tags, with bidirectional relationships in the SQLAlchemy models. Created a complete CRUD API for tags with all standard endpoints. Updated Note schemas to support tag associations via a `tag_ids` field that gets validated during create and patch operations. Added tag color validation using regex pattern for standard 6-digit hex colors. Configured cascade deletion so that when a tag is deleted, it's removed from all associated notes without deleting the notes themselves.

**Testing Performed:**
```bash
cd week7 && PYTHONPATH=. pytest backend/tests/test_tags.py -v
# Result: 11 tests passed
```

Added 11 comprehensive tests covering tag CRUD operations, duplicate tag name prevention, color format validation with multiple invalid formats, note-tag associations during create and update, cascade deletion behavior, and tag sorting.

**Notable Tradeoffs:**
No tag hierarchy or nesting support. Tags are global and not user-scoped. No limit on the number of tags per note. Deleting a tag removes it from all notes without confirmation.

### c. Graphite Diamond generated code review

**Many-to-many relationship setup** - Check the note_tags association table and bidirectional relationships in both Note and Tag models

**Tag name uniqueness** - Verify the duplicate prevention logic in tag creation and patch operations

**Color validation** - Ensure the hex color pattern ^#[0-9A-Fa-f]{6}$ is correct

**Tag association logic** - Review how notes handle tag_ids during create/patch, including validation that all tag IDs exist

**Cascade deletion behavior** - Confirm the ondelete="CASCADE" in the association table properly removes tags from notes

**Test coverage** - Verify all edge cases are tested (duplicate names, invalid colors, invalid tag IDs, cascade deletion)

---

## Task 4: Improve tests for pagination and sorting

### a. Links to relevant commits/issues
- Branch: `week7-task4-pagination-sorting-tests`
- PR: https://app.graphite.com/github/pr/sweetkruts/cs146s/4
- Commit: https://github.com/sweetkruts/cs146s/commit/46d2bfc

### b. PR Description
**Problem Statement:**
Existing tests didn't adequately cover edge cases for pagination and sorting functionality, leaving potential bugs undetected.

**Implementation Approach:**
Created a comprehensive test suite with 18 tests covering pagination edge cases including basic skip/limit functionality, skip values beyond available results, limit of zero, maximum limit enforcement (200 max with 422 error for exceeding), large skip values over 1 million, and boundary conditions. Also added sorting tests for ascending and descending order by various fields including title, description, and created_at, invalid field names with graceful fallback, sorting by boolean fields like completed status, and default sorting behavior. Included combination tests for pagination with sorting, search queries, and filtering by completion status.

**Testing Performed:**
```bash
cd week7 && PYTHONPATH=. pytest backend/tests/test_pagination_sorting.py -v
# Result: 18 tests passed
```

All tests passing with no regressions in existing functionality.

**Notable Tradeoffs:**
Tests create many database records (250 in one test) which may impact test suite performance. No performance benchmarking for large datasets with thousands of records.

### c. Graphite Diamond generated code review

**Test isolation** - Each test creates its own data but there's no cleanup between tests. Verify the client fixture properly resets the database.

**Timing-sensitive assertions** - Lines 67-82 test created_at sorting, which could be flaky if records are created too quickly and get identical timestamps.

**Invalid field fallback** - Line 87 tests invalid sorting but only checks status 200, not whether it actually falls back to the default -created_at behavior.

**Max limit validation** - Line 38 expects 422 for limit=250, but the actual limit enforcement is le=200 in the Query parameter. Verify this is the intended validation behavior.

**Search + pagination test** - Line 162 sets limit=1 but doesn't verify it returns the first result from the full search set (could add skip assertion).

**Performance** - Line 31 creates 250 records. Consider if this is necessary or if a smaller number would suffice.

---

## Brief Reflection 

### a. The types of comments I typically made in my manual reviews

During my manual reviews, I focused on whether the implementation actually makes sense from a user and system perspective. I questioned business logic decisions like why notes and action items have different validation rules, or whether the asymmetry between unlimited content length versus 500 character descriptions was intentional. I paid attention to API design and consistency across endpoints, making sure all resources follow similar patterns and return intuitive error messages. I also considered code architecture and whether the structure would scale as features are added, particularly around issues like code duplication and separation of concerns.

Security and data integrity were important, though mostly verified through proper ORM usage to prevent SQL injection and understanding cascade deletion implications. For testing, I cared less about raw coverage numbers and more about whether the tests would actually catch real bugs and remain maintainable as the codebase evolves. Performance considerations came up around database query efficiency and test execution speed, especially when seeing tests that create hundreds of records.

### b. Comparison of my comments vs. Graphite's AI-generated comments

Graphite focused heavily on verification and technical correctness. Most of its comments started with "Verify this" or "Confirm that" or "Check the", followed by specific implementation details, line numbers, and code-level issues like db.flush() versus db.commit() or regex patterns. It excelled at testing mechanics, pointing out exact assertions, status codes, and test behavior.

I approached reviews differently, asking "why" questions rather than just checking if things work. Where Graphite said "verify the duplicate prevention logic in tag creation", I wondered whether tag names should be case-insensitive since "Work" and "work" as separate tags might confuse users. When Graphite noted that timing tests could be flaky, I thought about how this would break in CI where tests run in parallel and whether we should mock datetime instead of relying on real timestamps.

The key difference is that Graphite gave me checklists while I tried to prioritize what actually matters. Graphite listed six items for Task 3 without indicating which were critical versus nice-to-have. When I noticed the missing GET endpoint for notes in Task 1, I flagged it as a blocker for API consistency that should be fixed before release. Graphite was thorough but literal, focusing on whether the implementation works correctly. I was more contextual, considering whether the design itself makes sense and what the implications are for users and maintainers.

### c. When the AI reviews were better/worse than mine

Graphite was significantly better at catching technical gotchas I would have missed. In Task 1, it caught that the test for GET /notes/{note_id} expects 404 after deletion but there's no explicit GET endpoint in the router. I would have completely missed this discrepancy between tests and implementation. The AI can systematically check test-code alignment in a way that's tedious for humans. It also excels at precise line references, pinpointing exactly where issues occur, which makes fixes much easier. For Task 3, it provided a comprehensive checklist of all six aspects to verify for the many-to-many relationship, ensuring nothing was forgotten. Pattern recognition is another strength - it immediately identified the !! versus ! logic issue and code duplication across three functions.

My reviews were better at understanding user intent and questioning whether requirements make sense in the first place. When I saw the validation asymmetry in Task 1, I didn't just note it - I questioned whether it was intentional and whether it would make sense to users. Graphite just said "confirm this matches requirements" without considering that the requirement itself might be flawed. I also noticed system-wide consistency issues that Graphite missed. While it focused on individual endpoints, I saw that notes and action items had inconsistent API patterns and suggested standardizing them. 

Prioritization is a major gap in AI reviews. I identified timing-sensitive tests as a blocker for CI/CD deployment, while Graphite just mentioned they could be flaky without conveying urgency. For design tradeoffs, I questioned whether we actually need three similar extraction functions or if we're over-engineering the solution. Graphite suggested consolidation but didn't challenge the original design decision. The user experience perspective is almost entirely missing from AI reviews. I considered whether we should warn users before cascade deleting tags from all notes, while Graphite only verified that the cascade behavior works technically.

The best example is the missing GET endpoint issue in Task 1. Graphite identified that notes lack a GET by ID endpoint while action items have one. I took it further and thought about how this inconsistency would confuse API consumers and which pattern should become the standard across all resources. For the code duplication in Task 2, Graphite flagged that three functions share logic and suggested consolidation. I wondered why we have three functions in the first place - is this requirement evolution? Should we deprecate old ones? Is backward compatibility needed? The timing tests in Task 4 show another difference: Graphite correctly identified they could be flaky, while I understood this would break in CI and block deployment.

### d. Comfort level trusting AI reviews and heuristics

I'd rate my current comfort level at about 6.5 out of 10. I trust AI reviews for catching things I might miss but not for deciding what actually matters or setting priorities.

AI reviews work well for initial code sweeps - that first pass to catch obvious issues around syntax, style, and missing edge cases. This is especially valuable in unfamiliar codebases where I don't know what to look for. They're also good for checklist verification, ensuring all test cases are covered and implementation details like regex patterns or status codes are correct. Pattern detection is another strength - finding code duplication and common antipatterns across large codebases where manual review would miss patterns. When debugging specific issues, AI's ability to catch test-implementation mismatches and provide precise error locations is helpful.

However, I would not rely on AI for design decisions. Questions like whether a feature should exist at all or if we're using the right architecture require human judgment. AI will tell you to verify something matches requirements, but it won't question whether the requirements themselves are wrong. User experience is another gap - AI checks if error messages exist but not if they're actually helpful or if the API is intuitive. Business logic needs human review because AI doesn't know your specific domain rules or edge cases unique to your business. Security is mixed - AI catches generic issues like SQL injection but misses domain-specific concerns like whether teachers should see all student data. And critically, AI lists everything equally without helping you triage what needs fixing before release versus what can wait.

My heuristic going forward is to run AI reviews first and let them catch the tedious stuff, freeing up my review time for design, UX, and business logic. For security, I trust AI for common vulnerabilities but always human-review authentication, authorization, and payment logic - AI is a safety net, not a security auditor. I think of it as AI providing breadth while I provide depth - AI scans everything quickly and might catch 80% of issues, while I dive deep on critical paths to catch the important 20%. When AI says "verify this matches requirements", that's my cue to ask whether the requirement should change, because AI assumes requirements are correct while humans can challenge them.

I also use AI's confidence level as a signal. If it gives specific line numbers and code examples, that's high trust. If it says "consider if...", that's low trust and needs human judgment. If it says "verify...", it doesn't actually know and I need to investigate.

Bottom line: AI code review is like autocorrect for code. It's great for catching typos and common mistakes, but you still need to read the message before sending it. I'd be comfortable merging a PR only if AI review found no major issues, I've personally reviewed the business logic and design, and another human has reviewed it. AI review alone is definitely not sufficient for production code.
