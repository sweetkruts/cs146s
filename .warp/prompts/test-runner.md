# Test Runner with Coverage

Run tests with comprehensive coverage analysis, flaky test detection, and actionable feedback.

## Usage

```
Run tests for {{week}} {{optional_test_path}}
```

## What This Does

1. **Navigate to the correct week directory** (week4 or week5)
2. **Run tests** with verbose output and early failure detection
3. **Analyze coverage** if tests pass
4. **Detect flaky tests** by running failed tests again
5. **Provide actionable feedback** with specific suggestions

## Steps

### 1. Validate and Navigate
- Determine which week directory to test (defaults to week4)
- Change to that directory: `cd /Users/willy/cs146s/modern-software-dev-assignments/{week}`

### 2. Run Initial Test Suite
```bash
PYTHONPATH=. pytest -v backend/tests {{test_path}} --maxfail=1 -x
```
- `-v`: Verbose output for detailed test names
- `--maxfail=1 -x`: Stop at first failure for fast feedback
- If `{{test_path}}` provided, test only that path

### 3. Handle Test Results

#### If All Tests Pass:
Run coverage analysis:
```bash
PYTHONPATH=. pytest backend/tests --cov=backend/app --cov-report=term-missing
```

Then provide:
- ✓ Total test count and pass rate
- ✓ Overall coverage percentage
- ✓ Files with <80% coverage (with missing line numbers)
- ✓ Suggestions for improving coverage

#### If Tests Fail:
**First, check for flaky tests:**
```bash
PYTHONPATH=. pytest -v {{failed_test_path}} --maxfail=3
```
- Re-run the failed test 3 times
- If it passes on retry, mark as potentially flaky
- If consistently fails, proceed with failure analysis

**Then provide failure analysis:**
- ⚠ Test name that failed
- ⚠ Failure reason (assertion error, exception, etc.)
- ⚠ Relevant code snippet from the test file
- ⚠ Relevant code snippet from implementation
- ⚠ 2-3 specific fixes ranked by likelihood
- ⚠ Offer to implement the most likely fix

### 4. Output Format

#### Success Output:
```
✓ Test Results: 15/15 passed (100%)
✓ Coverage: 92%

📊 Coverage by Module:
  - backend/app/routers/notes.py: 95% (missing: lines 42-45)
  - backend/app/routers/action_items.py: 88% (missing: lines 67, 89-91)
  - backend/app/services/extract.py: 100%

💡 Suggestions:
  1. Add tests for error handling in notes.py:42-45 (PUT endpoint edge case)
  2. Test action_items.py pagination with empty results
```

#### Failure Output:
```
⚠ Test Failed: test_update_note_not_found

🔍 Failure Analysis:
Issue: Expected 404 status code, got 500

Test code (test_notes.py:45-48):
    response = client.put("/notes/999", json={"content": "updated"})
    assert response.status_code == 404

Implementation (routers/notes.py:67-72):
    note = db.query(Note).filter(Note.id == note_id).first()
    note.content = updated_data.content  # Fails if note is None
    
🔧 Suggested Fixes (ranked):
  1. Add null check before accessing note.content (HIGH CONFIDENCE)
     → if not note: raise HTTPException(status_code=404, detail="Note not found")
  
  2. Use .one_or_none() instead of .first() with explicit error handling
  
  3. Add database-level constraint validation

Would you like me to implement fix #1?
```

#### Flaky Test Output:
```
⚠ Flaky Test Detected: test_concurrent_updates

🔄 Test passed 2/3 times on retry

Possible causes:
  1. Race condition in concurrent database writes
  2. Timing-dependent assertion
  3. Shared test state not properly isolated

Recommendations:
  - Add @pytest.mark.flaky(reruns=3) decorator
  - Review test for timing assumptions
  - Check fixture teardown/setup
```

## Safety Guidelines

- ✓ Read-only by default (only runs tests)
- ✓ Never modifies code without explicit user approval
- ✓ Preserves test isolation
- ✓ Does not commit changes automatically

## Arguments

- `{{week}}`: week4 or week5 (default: week4)
- `{{optional_test_path}}`: Specific test file or function (e.g., `test_notes.py::test_create_note`)

## Examples

```
Run tests for week4
Run tests for week5 test_notes.py
Run tests for week4 test_notes.py::test_update_note_success
```
