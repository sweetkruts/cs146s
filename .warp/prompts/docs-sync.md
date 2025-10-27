# Docs Sync: API Documentation from OpenAPI

Automatically generate or update `docs/API.md` from the OpenAPI spec and identify route deltas (new, changed, or removed endpoints).

## Usage

```
Sync API docs for {{week}}
```

## What This Does

1. **Fetch the current OpenAPI specification** from running server or generate it
2. **Compare with existing API.md** to detect changes
3. **Generate/update API.md** with all endpoint documentation
4. **List route deltas** (new, modified, removed endpoints)
5. **Validate documentation completeness**

## Steps

### 1. Ensure Server is Running
```bash
cd /Users/willy/cs146s/modern-software-dev-assignments/{{week}}
# Check if server is already running
lsof -i :8000 | grep LISTEN || (PYTHONPATH=. uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 &)
sleep 2  # Wait for server startup
```

### 2. Fetch OpenAPI Specification
```bash
curl -s http://localhost:8000/openapi.json > /tmp/openapi_current.json
```

If server isn't running, generate spec directly:
```bash
PYTHONPATH=. python -c "from backend.app.main import app; import json; print(json.dumps(app.openapi(), indent=2))" > /tmp/openapi_current.json
```

### 3. Parse Current API Documentation
- Read existing `docs/API.md` if it exists
- Extract documented endpoints (paths and methods)
- Store as baseline for comparison

### 4. Parse OpenAPI Spec
Extract from `/tmp/openapi_current.json`:
- All paths and methods (GET, POST, PUT, DELETE)
- Parameters (path, query, body)
- Request schemas
- Response schemas and status codes
- Descriptions and summaries
- Tags for grouping

### 5. Detect Route Deltas
Compare OpenAPI spec with existing docs:

**New Endpoints:**
- In OpenAPI spec but not in API.md
- Mark with 🆕 emoji

**Modified Endpoints:**
- Same path/method but different parameters or responses
- Mark with ⚠️ emoji

**Removed Endpoints:**
- In API.md but not in OpenAPI spec
- Mark with ❌ emoji

**Unchanged Endpoints:**
- Same in both, mark with ✓

### 6. Generate API.md
Create structured documentation:

```markdown
# API Documentation

Last updated: {timestamp}
Generated from OpenAPI spec version {version}

## Overview
{app_description}

Base URL: `http://localhost:8000`

## Endpoints

### Notes
#### GET /notes
**Description:** List all notes

**Response:** 200 OK
```json
[
  {
    "id": 1,
    "content": "Example note",
    "created_at": "2025-01-27T12:00:00"
  }
]
```

**Response Schema:**
- `id` (integer): Unique note identifier
- `content` (string): Note content
- `created_at` (string): ISO 8601 timestamp

**Error Responses:**
- 500: Internal server error

---

[Continue for each endpoint...]
```

### 7. Output Route Delta Report
```
📊 API Documentation Sync Report

✓ Unchanged: 6 endpoints
🆕 New: 2 endpoints
  - POST /notes/{note_id}/tags
  - GET /action-items/search

⚠️  Modified: 1 endpoint
  - PUT /notes/{note_id}
    Changes: Added optional 'tags' field to request body

❌ Removed: 0 endpoints

📝 Documentation Coverage:
  - Total endpoints: 9
  - Documented: 9 (100%)
  - Missing descriptions: 0
  - Missing examples: 1 (GET /action-items/search)

💡 Recommendations:
  1. Add request/response examples for GET /action-items/search
  2. Consider adding rate limit documentation
```

### 8. Update API.md
- Write new content to `docs/API.md`
- Preserve any manual sections (e.g., authentication, rate limits)
- Add generation timestamp at top
- Format with consistent markdown style

## Output Format

### Success:
```
✅ API documentation synced successfully

📄 Updated: docs/API.md
📊 Total endpoints documented: 9
🆕 New endpoints: 2
⚠️  Modified endpoints: 1

Review the changes and commit when ready.
```

### With Warnings:
```
⚠️  API documentation synced with warnings

📄 Updated: docs/API.md
📊 Total endpoints documented: 9

⚠️  Issues found:
  1. POST /notes missing request body example
  2. GET /action-items has no description
  3. DELETE /notes/{note_id} response schema incomplete

💡 Suggested fixes:
  - Add docstrings to endpoint functions
  - Use response_model in @router decorators
  - Add examples in Pydantic schemas
```

## Idempotency

- ✓ Multiple runs produce identical output for same spec
- ✓ Preserves manual documentation sections
- ✓ Safe to run repeatedly without side effects
- ✓ Does not commit changes automatically

## Safety Guidelines

- ✓ Backs up existing API.md before overwriting
- ✓ Validates JSON schema before generation
- ✓ Never modifies source code
- ✓ Only writes to docs/ directory

## Arguments

- `{{week}}`: week4 or week5 (default: week4)

## Examples

```
Sync API docs for week4
Sync API docs for week5
```

## Advanced: Manual Sections Preservation

The sync process preserves these sections if they exist in API.md:
- `## Authentication` - Auth requirements
- `## Rate Limiting` - Rate limit policies
- `## Error Codes` - Standard error reference
- `## Pagination` - Pagination conventions

These sections are detected by heading markers and re-inserted after sync.
