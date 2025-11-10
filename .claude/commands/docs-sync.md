# Documentation Sync

Synchronize API documentation with the actual OpenAPI specification.

## Usage
```
/docs-sync
```

## Steps

1. **Navigate to week4 directory**
   ```bash
   cd /Users/willy/cs146s/modern-software-dev-assignments/week4
   ```

2. **Start the FastAPI server (if not running)**
   - Check if server is running on port 8000
   - If not, start it in background: `make run &`
   - Wait 3 seconds for server to initialize

3. **Fetch current OpenAPI spec**
   ```bash
   curl -s http://localhost:8000/openapi.json
   ```

4. **Read existing API documentation**
   - Check if `docs/API.md` exists
   - If it exists, read the current content
   - If not, note that it needs to be created

5. **Compare and generate documentation**
   - Extract all endpoints from OpenAPI spec
   - For each endpoint, document:
     - Method and path
     - Description
     - Request body schema (if applicable)
     - Response schema
     - Status codes
   - Compare with existing docs to identify:
     - New endpoints not yet documented
     - Changed endpoints (different schemas/descriptions)
     - Removed endpoints (documented but no longer in spec)

6. **Update API.md**
   - Create or update `docs/API.md` with:
     - Table of contents
     - Grouped endpoints by tag
     - Full details for each endpoint
   - Preserve any custom notes or examples in existing docs

7. **Generate change summary**
   ```
   📝 Documentation Sync Results
   
   ✨ New endpoints:
   - [method] /path - description
   
   🔄 Updated endpoints:
   - [method] /path - what changed
   
   ❌ Removed endpoints:
   - [method] /path
   
   📄 Updated: docs/API.md
   ```

8. **Update TASKS.md if needed**
   - Add any TODOs for incomplete endpoint implementations
   - Note any validation or error handling gaps

## Safety
- Creates/updates documentation files only
- Preserves existing custom content where possible
- Does not modify application code






