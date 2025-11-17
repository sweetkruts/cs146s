# Add API Endpoint

Guided workflow to add a new API endpoint following TDD best practices.

## Usage
```
/add-endpoint [resource] [method] [path]
```

Example: `/add-endpoint note PUT /notes/{note_id}`

## Steps

1. **Parse and validate arguments**
   - Extract resource name, HTTP method, and path from `$ARGUMENTS`
   - Determine which router file to modify (e.g., notes.py for /notes/*)
   - Identify the relevant model and schemas

2. **Write failing test first (TDD)**
   - Navigate to `backend/tests/test_[resource].py`
   - Create a new test function: `test_[method]_[resource]`
   - Test should:
     - Set up test data if needed
     - Make the API request
     - Assert expected status code
     - Assert response structure
     - Assert business logic results
   - Run the test to confirm it fails (endpoint doesn't exist yet)

3. **Implement the endpoint**
   - Open `backend/app/routers/[resource].py`
   - Add the new route handler:
     - Proper decorator with method, path, response_model
     - Type hints for parameters and return value
     - DB session dependency
     - Error handling (404, 400, etc.)
     - Business logic implementation
   - Follow existing code style in the file

4. **Add/update schemas if needed**
   - Check if new Pydantic schemas are needed in `schemas.py`
   - Add request/response models if they don't exist
   - Use proper validation (min_length, etc.)

5. **Run tests to verify**
   - Run the new test: `PYTHONPATH=. pytest backend/tests/test_[resource].py::test_[method]_[resource] -v`
   - If it fails, debug and fix
   - Run full test suite: `make test`

6. **Update frontend if applicable**
   - Check `frontend/app.js` to see if UI integration is needed
   - Add fetch call for the new endpoint
   - Update UI to use the new functionality
   - Test manually at http://localhost:8000

7. **Run linting**
   ```bash
   make format
   make lint
   ```

8. **Summary output**
   ```
   ✅ New endpoint added: [METHOD] /path
   
   Files modified:
   - backend/app/routers/[resource].py
   - backend/tests/test_[resource].py
   - backend/app/schemas.py (if applicable)
   - frontend/app.js (if applicable)
   
   ✓ Tests passing
   ✓ Linting clean
   
   Next steps:
   - Test manually at http://localhost:8000
   - Run /docs-sync to update API documentation
   ```

## Best Practices
- Always write tests first (TDD)
- Use proper type hints
- Include error handling
- Follow existing code patterns
- Run full test suite before finishing

## Safety
- Stops at first failing test
- Requires test to pass before considering complete
- Preserves existing functionality
- Uses black/ruff for consistent formatting







