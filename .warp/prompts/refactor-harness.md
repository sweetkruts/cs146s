# Refactor Harness: Safe Module Refactoring

Safely refactor modules, classes, or functions with automatic import updates, linting, and comprehensive test validation.

## Usage

```
Refactor {{old_name}} to {{new_name}} in {{week}}
```

## What This Does

1. **Plan the refactoring** (preview affected files)
2. **Rename the module/class/function**
3. **Update all imports automatically**
4. **Run linter** to catch syntax issues
5. **Run full test suite** to validate behavior
6. **Rollback if issues detected**

## Steps

### 1. Pre-flight Validation
```bash
cd /Users/willy/cs146s/modern-software-dev-assignments/{{week}}
```

**Validate inputs:**
- Check `{{old_name}}` exists (file, class, or function)
- Verify `{{new_name}}` doesn't conflict with existing names
- Identify file type (module, class, function)

**Find all references:**
```bash
# For module rename
grep -r "from.*{{old_name}}" backend/ --include="*.py" | wc -l

# For function/class rename  
grep -r "{{old_name}}" backend/ --include="*.py" | wc -l
```

**Show preview:**
```
🔍 Refactoring Preview

Type: Module rename
Old: backend/app/services/extract.py
New: backend/app/services/extraction.py

📝 Files to update: 5
  - backend/app/routers/action_items.py (1 import)
  - backend/tests/test_extract.py (3 references)
  - backend/tests/test_action_items.py (1 import)
  - backend/app/main.py (0 references)
  - backend/app/services/__init__.py (1 export)

⚠️  Risk assessment: LOW
  - All changes are import statements
  - No external API changes
  - Full test coverage exists

Proceed? (y/n)
```

### 2. Create Backup
```bash
# Create backup branch
git stash
git checkout -b refactor/{{old_name}}-to-{{new_name}}-$(date +%Y%m%d-%H%M%S)

# Store original file hashes for rollback
find backend/ -name "*.py" -type f -exec md5 {} \; > /tmp/refactor_backup_hashes.txt
```

### 3. Execute Refactoring

#### For Module Rename:
```bash
# Rename the file
git mv backend/app/services/{{old_name}}.py backend/app/services/{{new_name}}.py
```

Then update all imports:
```python
# Find and replace pattern:
# OLD: from backend.app.services.{{old_name}} import
# NEW: from backend.app.services.{{new_name}} import

# OLD: from .services.{{old_name}} import
# NEW: from .services.{{new_name}} import
```

#### For Class/Function Rename:
Use AST-based refactoring to preserve structure:
```bash
PYTHONPATH=. python << 'EOF'
import ast
import astor

# Parse and refactor each affected file
# Update class/function definitions
# Update all references
# Preserve comments and formatting
EOF
```

### 4. Update Imports Systematically

**Pattern 1: Absolute imports**
```python
# Before
from backend.app.services.extract import extract_action_items

# After
from backend.app.services.extraction import extract_action_items
```

**Pattern 2: Relative imports**
```python
# Before
from ..services.extract import extract_action_items

# After  
from ..services.extraction import extract_action_items
```

**Pattern 3: Module imports**
```python
# Before
import backend.app.services.extract as extract

# After
import backend.app.services.extraction as extract
```

**Pattern 4: Star imports (discouraged but handle)**
```python
# Before
from backend.app.services.extract import *

# After
from backend.app.services.extraction import *
```

### 5. Run Linter
```bash
make lint
```

**If linter fails:**
- Show specific errors with line numbers
- Attempt auto-fix: `make format`
- Re-run linter
- If still failing, show errors and ask for manual review

### 6. Run Full Test Suite
```bash
make test
```

**Test validation criteria:**
- All tests must pass
- No new warnings
- Coverage should not decrease

**If tests fail:**
```
⚠️  Tests failed after refactoring

Failed tests:
  - test_extract::test_extract_action_items_heuristic
    Error: ImportError: cannot import name 'extract_action_items'
    
🔧 Auto-fix attempt:
  - Checking for missed import updates...
  - Found: backend/tests/conftest.py line 12
  - Updating import statement
  - Rerunning tests...
```

### 7. Verify No Broken References
```bash
# Check for any remaining old references
grep -r "{{old_name}}" backend/ --include="*.py" | grep -v "{{new_name}}"
```

If found:
```
⚠️  Found lingering references:
  - backend/tests/test_integration.py:45 (comment)
  - backend/README.md:12 (documentation)

These are non-code references. Update manually? (y/n)
```

### 8. Generate Refactoring Summary
```
✅ Refactoring completed successfully

📦 Changes:
  Module renamed: extract.py → extraction.py
  
📝 Files modified: 5
  ✓ backend/app/services/extraction.py (renamed)
  ✓ backend/app/routers/action_items.py (import updated)
  ✓ backend/tests/test_extract.py (import updated)
  ✓ backend/tests/test_action_items.py (import updated)
  ✓ backend/app/services/__init__.py (export updated)

✅ Validation:
  ✓ Linter: PASSED (0 errors)
  ✓ Tests: PASSED (15/15)
  ✓ Coverage: 92% (unchanged)
  ✓ No broken references found

📊 Git status:
  - 1 file renamed
  - 4 files modified
  - Branch: refactor/extract-to-extraction-20251027-120000

💡 Next steps:
  1. Review changes: git diff HEAD~1
  2. Run application manually to verify
  3. Commit changes: git commit -m "Refactor: Rename extract to extraction"
  4. Merge to main when ready
```

## Rollback Procedure

If any step fails critically:
```bash
# Restore from backup
git reset --hard HEAD
git checkout main
git branch -D refactor/{{old_name}}-to-{{new_name}}-*

# Restore stashed changes
git stash pop
```

Report rollback:
```
❌ Refactoring rolled back

Reason: Tests failed after 3 auto-fix attempts

The repository has been restored to its original state.

Failures encountered:
  1. test_integration.py import error (line 45)
  2. Circular dependency detected in new structure

💡 Suggestions:
  - Review circular dependencies before retrying
  - Consider splitting module into smaller units
  - Update test fixtures to use new structure
```

## Safety Guidelines

- ✓ Creates backup branch automatically
- ✓ Validates before executing changes
- ✓ Runs comprehensive tests after changes
- ✓ Rolls back on failure
- ✓ Never force-pushes
- ✓ Preserves git history

## Idempotency

- ✓ Can be run multiple times safely
- ✓ Detects if refactoring already completed
- ✓ No side effects on repeated runs

## Arguments

- `{{old_name}}`: Current name (module, class, or function)
- `{{new_name}}`: New name
- `{{week}}`: week4 or week5 (default: week4)

## Examples

```
Refactor extract to extraction in week4
Refactor ActionItem to Task in week5
Refactor get_db to get_database_session in week4
```

## Advanced: Partial Refactoring

For selective refactoring (e.g., rename in specific files only):
```
Refactor {{old_name}} to {{new_name}} in {{week}} files {{file_pattern}}
```

Example:
```
Refactor extract to extraction in week4 files backend/app/services/*
```

This limits changes to matching files only.
