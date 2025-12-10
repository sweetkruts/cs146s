# Test Suite Runner

Run the test suite with detailed reporting and actionable feedback.

## Usage
```
/test-suite [optional: specific test path or marker]
```

## Steps

1. **Change to week4 directory**
   ```bash
   cd /Users/willy/cs146s/modern-software-dev-assignments/week4
   ```

2. **Run tests with pytest**
   - If `$ARGUMENTS` is provided, run: `PYTHONPATH=. pytest -v backend/tests/$ARGUMENTS --maxfail=1 -x`
   - Otherwise, run: `PYTHONPATH=. pytest -v backend/tests --maxfail=1 -x`
   - The `-x` flag stops at first failure for faster feedback
   - The `--maxfail=1` ensures we stop early

3. **Analyze results**
   - If all tests pass:
     - Run coverage: `PYTHONPATH=. pytest backend/tests --cov=backend/app --cov-report=term-missing`
     - Summarize coverage percentage
     - Identify any files with < 80% coverage
     - Suggest areas for additional testing
   - If tests fail:
     - Identify which test failed and why
     - Show the relevant code section
     - Suggest 2-3 specific fixes
     - Offer to implement the fix

4. **Output format**
   ```
   ✓ Test Results: [X/Y passed]
   ✓ Coverage: [Z%]
   
   [If failures]
   ⚠ Failed: test_name
   Issue: [description]
   Suggested fixes:
   1. [fix 1]
   2. [fix 2]
   
   [If low coverage]
   📊 Low coverage files:
   - file.py: [coverage%] - Missing: [lines]
   ```

## Safety
- Read-only by default (just runs tests)
- Does not modify code unless explicitly approved
- Always preserves test isolation







