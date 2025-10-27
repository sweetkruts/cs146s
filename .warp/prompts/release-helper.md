# Release Helper: Prepare Releases

Automate release preparation including version bumps, pre-release checks, changelog generation, and validation.

## Usage

```
Prepare release {{version_type}} for {{week}}
```

Where `{{version_type}}` is: `major`, `minor`, `patch`, or specific version like `1.2.3`

## What This Does

1. **Validate repository state** (clean working tree, on main branch)
2. **Determine new version number**
3. **Run comprehensive pre-release checks** (tests, lint, coverage)
4. **Generate changelog snippet** from git commits
5. **Update version in relevant files**
6. **Create release commit and tag**
7. **Provide next-step instructions**

## Steps

### 1. Pre-Release Validation

```bash
cd /Users/willy/cs146s/modern-software-dev-assignments/{{week}}

# Check git status
git status --porcelain
```

**Validation checks:**
- ✓ Working tree is clean (no uncommitted changes)
- ✓ On main/master branch (or explicit release branch)
- ✓ Up to date with remote (no unpulled changes)
- ✓ No merge conflicts

**If validation fails:**
```
⚠️  Pre-release validation failed

Issues found:
  ❌ Uncommitted changes detected:
     - backend/app/main.py (modified)
     - backend/tests/test_notes.py (modified)
  
  ❌ Current branch: feature/add-tags (expected: main)

💡 Required actions:
  1. Commit or stash your changes
  2. Switch to main branch: git checkout main
  3. Pull latest changes: git pull origin main
  
Retry after fixing these issues.
```

### 2. Determine Version Number

**Current version detection:**
Read from `pyproject.toml`:
```bash
grep "^version =" pyproject.toml | cut -d'"' -f2
```

**Version bump logic:**
- Current: `0.1.0`
- `major`: → `1.0.0`
- `minor`: → `0.2.0`
- `patch`: → `0.1.1`
- Specific (e.g., `1.5.2`): → `1.5.2`

**Show version plan:**
```
📦 Release Version Plan

Current version: 0.1.0
New version: 0.2.0 (minor bump)

Version follows semantic versioning:
  - MAJOR: Breaking changes
  - MINOR: New features (backward compatible)
  - PATCH: Bug fixes

Proceed with v0.2.0? (y/n)
```

### 3. Run Pre-Release Checks

#### Check 1: Full Test Suite
```bash
make test
```
- All tests must pass
- No test failures allowed
- Must complete without errors

#### Check 2: Linting
```bash
make lint
```
- No linting errors
- Code style compliance
- No unresolved warnings

#### Check 3: Coverage Analysis
```bash
PYTHONPATH=. pytest backend/tests --cov=backend/app --cov-report=term
```
- Minimum 80% coverage required
- No coverage regressions from previous version

#### Check 4: Type Checking (if available)
```bash
# Check if mypy is configured
if command -v mypy &> /dev/null; then
    PYTHONPATH=. mypy backend/app
fi
```

**Report checks:**
```
✅ Pre-Release Checks

✓ Tests: PASSED (15/15)
✓ Linting: PASSED (0 errors, 0 warnings)
✓ Coverage: 92% (target: ≥80%)
✓ Type checking: PASSED (optional)

All checks passed! Ready to proceed with release.
```

**If any check fails:**
```
❌ Pre-Release Check Failed

Check: Tests
Status: FAILED (3 failures)

Failed tests:
  - test_notes::test_create_note_invalid
  - test_action_items::test_update_item
  - test_integration::test_full_workflow

❌ Release blocked

You must fix all test failures before releasing.
Run this for details: make test

Suggestions:
  1. Fix failing tests
  2. Run release helper again after fixes
```

### 4. Generate Changelog Snippet

Extract commits since last release:
```bash
# Get last release tag
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")

# Generate changelog from commits
if [ -n "$LAST_TAG" ]; then
    git log $LAST_TAG..HEAD --pretty=format:"- %s (%h)" --no-merges
else
    git log --pretty=format:"- %s (%h)" --no-merges --max-count=20
fi
```

**Categorize commits:**
- 🎉 **Features**: Commits with `feat:`, `feature:`
- 🐛 **Fixes**: Commits with `fix:`, `bugfix:`
- ♻️ **Refactor**: Commits with `refactor:`
- 📝 **Docs**: Commits with `docs:`, `doc:`
- ✅ **Tests**: Commits with `test:`, `tests:`
- 🔧 **Chore**: Other commits

**Generate formatted changelog:**
```markdown
## [0.2.0] - 2025-01-27

### Features
- Add pagination to notes endpoint (a1b2c3d)
- Implement action item filtering by status (d4e5f6g)

### Fixes
- Fix null pointer in note update handler (g7h8i9j)
- Correct timestamp formatting in API responses (j1k2l3m)

### Refactor
- Rename extract module to extraction (m4n5o6p)

### Documentation
- Update API.md with new endpoints (p7q8r9s)

### Tests
- Add integration tests for note CRUD (s1t2u3v)
```

**Save to file:**
```bash
# Append to CHANGELOG.md
cat > /tmp/changelog_snippet.md << 'EOF'
[Generated changelog content]
EOF

# Prepend to existing CHANGELOG.md or create new
if [ -f CHANGELOG.md ]; then
    cat /tmp/changelog_snippet.md CHANGELOG.md > /tmp/changelog_new.md
    mv /tmp/changelog_new.md CHANGELOG.md
else
    mv /tmp/changelog_snippet.md CHANGELOG.md
fi
```

### 5. Update Version in Files

**Files to update:**

1. `pyproject.toml`:
```bash
sed -i '' 's/^version = ".*"/version = "0.2.0"/' pyproject.toml
```

2. `backend/app/main.py` (if version is defined):
```python
# Update FastAPI app version
app = FastAPI(title="...", version="0.2.0")
```

3. Any other version references:
```bash
# Search for hardcoded versions
grep -r "0\.1\.0" backend/ --include="*.py"
```

**Show diff:**
```
📝 Version Updates

Files modified:
  M pyproject.toml
    - version = "0.1.0"
    + version = "0.2.0"
  
  M backend/app/main.py
    - app = FastAPI(title="...", version="0.1.0")
    + app = FastAPI(title="...", version="0.2.0")
```

### 6. Create Release Commit and Tag

```bash
# Stage version changes
git add pyproject.toml backend/app/main.py CHANGELOG.md

# Create release commit
git commit -m "Release v0.2.0

- Bump version to 0.2.0
- Update changelog for v0.2.0 release
- Include all changes from [last_tag]..HEAD"

# Create annotated tag
git tag -a v0.2.0 -m "Release version 0.2.0

See CHANGELOG.md for details."
```

**Show git status:**
```
📊 Git Status

✓ Release commit created:
  commit abc123def456
  Release v0.2.0

✓ Tag created: v0.2.0

📦 Ready to push:
  - 1 commit
  - 1 tag
```

### 7. Final Instructions

```
✅ Release v0.2.0 prepared successfully!

📋 Summary:
  Version: 0.1.0 → 0.2.0
  Commits: 12 since last release
  Tests: PASSED (15/15)
  Coverage: 92%
  
📝 Changes:
  - 3 features added
  - 2 bugs fixed
  - 1 refactor
  - 2 documentation updates

📦 Files updated:
  - pyproject.toml
  - backend/app/main.py
  - CHANGELOG.md

🏷️  Git tag: v0.2.0
✓ Commit: abc123def456

📤 Next Steps:
  1. Review the changes:
     git show v0.2.0
     git diff v0.1.0..v0.2.0
  
  2. Push to remote (when ready):
     git push origin main
     git push origin v0.2.0
  
  3. (Optional) Create GitHub release:
     gh release create v0.2.0 --notes-file CHANGELOG.md
  
  4. (Optional) Publish to PyPI (if configured):
     poetry publish --build

⚠️  Important: Review all changes before pushing!
```

## Rollback Procedure

If you need to undo the release preparation:
```bash
# Remove the tag
git tag -d v0.2.0

# Reset to previous commit
git reset --hard HEAD~1

# Restore files
git checkout HEAD -- pyproject.toml backend/app/main.py CHANGELOG.md
```

## Safety Guidelines

- ✓ Never pushes automatically (requires manual confirmation)
- ✓ Validates all checks before proceeding
- ✓ Creates backup tags before changes
- ✓ Preserves complete git history
- ✓ Generates changelog from actual commits
- ✓ Requires clean working tree

## Idempotency

- ✓ Detects if release already exists
- ✓ Can be safely re-run after fixes
- ✓ Won't create duplicate tags
- ✓ Preserves existing changelog entries

## Arguments

- `{{version_type}}`: `major`, `minor`, `patch`, or specific version (e.g., `1.2.3`)
- `{{week}}`: week4 or week5 (default: week4)

## Examples

```
Prepare release minor for week4
Prepare release patch for week5
Prepare release 1.0.0 for week4
Prepare release major for week5
```

## Advanced Options

### Dry Run
Preview changes without committing:
```
Prepare release minor for week4 --dry-run
```

### Skip Checks
Skip specific checks (not recommended):
```
Prepare release patch for week4 --skip-tests
```

### Custom Changelog
Use manual changelog instead of auto-generated:
```
Prepare release minor for week4 --changelog-file custom_notes.md
```
