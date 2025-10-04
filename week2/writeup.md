# Week 2 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: **William Li** \
SUNet ID: **06682547** \
Citations: **Sonnet 4.5**

This assignment took me about **1** hours to do. 


## YOUR RESPONSES
For each exercise, please include what prompts you used to generate the answer, in addition to the location of the generated response. Make sure to clearly add comments in your code documenting which parts are generated.

### Exercise 1: Scaffold a New Feature
Prompt: 
```
Analyze the heuristics in extract action items

Then, complete this: (pasted the requirements from assignment here)
``` 

Generated Code Snippets:
```
File: week2/app/services/extract.py
- Lines 92-179: Complete extract_action_items_llm() function
  - Function definition with type hints and docstring (92-108)
  - Empty input validation (109-111)
  - JSON schema definition for structured output (113-126)
  - Prompt engineering for action item extraction (128-139)
  - Ollama API call with error handling (141-178)
  - Deduplication logic (162-173)

Key features generated:
- Ollama chat integration with structured JSON output
- Temperature setting for consistency (0.1)
- Comprehensive error handling with JSON parsing
- Deduplication based on case-insensitive matching
```

### Exercise 2: Add Unit Tests
Prompt: 
```
(Continued from Exercise 1 - part of the same conversation in Cursor)
The AI automatically generated comprehensive unit tests after implementing the LLM function.
``` 

Generated Code Snippets:
```
File: week2/tests/test_extract.py
- Lines 4: Added import for extract_action_items_llm
- Lines 22-176: Nine comprehensive test functions for LLM extraction

Test functions generated:
1. test_llm_extract_bullet_list (lines 26-42)
   - Tests standard bullet point extraction
   
2. test_llm_extract_keyword_prefixed (lines 45-59)
   - Tests TODO, Action, Next keywords
   
3. test_llm_extract_empty_input (lines 62-70)
   - Tests empty string and whitespace handling
   
4. test_llm_extract_no_action_items (lines 73-84)
   - Tests text with no action items
   
5. test_llm_extract_mixed_format (lines 87-106)
   - Tests combination of formats (bullets, checkboxes, keywords)
   
6. test_llm_extract_numbered_list (lines 109-126)
   - Tests numbered list extraction
   
7. test_llm_extract_imperative_sentences (lines 129-144)
   - Tests imperative verb detection
   
8. test_llm_extract_deduplication (lines 147-158)
   - Tests case-insensitive deduplication
   
9. test_llm_extract_checkbox_markers (lines 161-175)
   - Tests [ ], [x], [todo] markers

All tests use flexible assertions with "any()" to account for LLM variability.
Test results: 10/10 passed in 5.67s
```

### Exercise 3: Refactor Existing Code for Clarity
Prompt: 
```
TODO 3: Refactor Existing Code for Clarity

Perform a refactor of the code in the backend, focusing in particular on well-defined API 
contracts/schemas, database layer cleanup, app lifecycle/configuration, error handling.
``` 

Generated/Modified Code Snippets:
```
1. NEW FILE: week2/app/schemas.py (149 lines)
   - Lines 1-149: Complete Pydantic schema definitions
   - NoteCreate, NoteResponse schemas (lines 16-47)
   - ActionItemExtractRequest, ActionItemResponse (lines 55-87)
   - ActionItemExtractResponse, ActionItemUpdateRequest (lines 90-118)
   - ActionItemUpdateResponse, ErrorResponse (lines 121-149)

2. NEW FILE: week2/app/config.py (65 lines)
   - Lines 1-65: Configuration management system
   - Settings class with environment variable support (lines 15-63)
   - Database path helpers (lines 44-59)
   - Global settings instance (line 63)

3. REFACTORED: week2/app/db.py (328 lines)
   - Lines 1-79: Added imports, logging, custom exceptions
     - DatabaseError, NoteNotFoundError, ActionItemNotFoundError (lines 22-37)
     - Context manager for connections with auto commit/rollback (lines 50-79)
   - Lines 82-138: Enhanced init_db() with indexes and error handling
   - Lines 141-220: Refactored note functions with validation and logging
     - insert_note with validation (lines 141-167)
     - list_notes with logging (lines 170-189)
     - get_note with logging (lines 192-220)
   - Lines 223-325: Refactored action item functions
     - insert_action_items with validation (lines 223-260)
     - list_action_items with logging (lines 263-293)
     - mark_action_item_done with row count checking (lines 296-325)

4. REFACTORED: week2/app/main.py (118 lines)
   - Lines 1-28: Added logging configuration
   - Lines 31-51: Async lifespan manager for startup/shutdown
   - Lines 54-61: FastAPI app with lifespan integration
   - Lines 69-86: Global error handlers for DatabaseError and ValueError
   - Lines 94-108: Added index() and health_check() endpoints
   - Lines 111-118: Router and static file mounting

5. REFACTORED: week2/app/routers/notes.py (153 lines)
   - Lines 1-27: Updated imports with Pydantic schemas and logging
   - Lines 30-74: Refactored create_note() with schemas and error handling
   - Lines 77-116: Refactored get_single_note() with proper responses
   - Lines 119-150: NEW: list_all_notes() endpoint

6. REFACTORED: week2/app/routers/action_items.py (235 lines initially, before TODO 4)
   - Lines 1-36: Updated imports and router configuration
   - Lines 39-91: Refactored extract() with schemas
   - Lines 94-132: Refactored list_all() with Query parameters
   - Lines 135-174: Refactored mark_done() with error handling

Key improvements:
- Type safety with Pydantic models throughout
- Comprehensive error handling with custom exceptions
- Proper logging at all levels
- Context manager for database connections
- Configuration via environment variables
- Database indexes for performance
- Application lifespan management
```


### Exercise 4: Use Agentic Mode to Automate a Small Task
Prompt: 
```
TODO4:

Integrate the LLM-powered extraction as a new endpoint. Update the frontend to include an 
"Extract LLM" button that, when clicked, triggers the extraction process via the new endpoint.

Expose one final endpoint to retrieve all notes. Update the frontend to include a "List Notes" 
button that, when clicked, fetches and displays them.
``` 

Generated Code Snippets:
```
1. MODIFIED: week2/app/routers/action_items.py
   - Line 25: Added import for extract_action_items_llm
   - Lines 39-94: NEW extract_llm() endpoint
     - POST /action-items/extract-llm
     - Full function with LLM integration
     - Error handling and logging
     - Same schema as heuristic extraction

2. MODIFIED: week2/frontend/index.html
   A. Updated Styles (lines 7-25):
      - Lines 10: Added h2 styling
      - Lines 12-15: Enhanced button styles with hover effects
      - Lines 18-21: Added note-item card styling
      - Line 24: Added section divider styling
   
   B. Updated HTML Structure (lines 31-45):
      - Line 35: Changed button text to "Extract (Heuristic)"
      - Line 36: NEW "Extract (LLM)" button with secondary class
      - Lines 41-45: NEW "Saved Notes" section with List Notes button
   
   C. Refactored JavaScript (lines 47-132):
      - Line 50: Added notesEl variable
      - Lines 52-89: NEW extractItems() generic handler function
      - Lines 91-99: Wired up both extract buttons to use handler
      - Lines 101-125: NEW listNotes button handler
        - Fetches from GET /notes endpoint
        - Renders notes as cards with ID, timestamp, content
      - Lines 127-132: NEW escapeHtml() security helper

Key features:
- Dual extraction buttons (Heuristic vs LLM)
- Notes listing with card-based UI
- Improved error handling and user feedback
- HTML escaping for security
- Loading states for better UX
```


### Exercise 5: Generate a README from the Codebase
Prompt: 
```
Now, analyze the entier codebase and generate a well-structured README.md file. focus on the changes we made as well as new files created. The README should include at least these:

A brief overview of the project
How to set up and run the project
API endpoints and functionality
Instructions for running the test suite

It should be clear. Well documented. Include other topics as you see fit.
``` 

Generated Code Snippets:
```
NEW FILE: week2/README.md (638 lines, 14 KB)

Structure:
- Lines 1-10: Title and overview
- Lines 12-33: Features section with extraction methods
- Lines 35-49: Tech stack listing
- Lines 51-79: Prerequisites (Python, Poetry, Ollama)
- Lines 81-113: Setup & installation instructions
- Lines 115-143: Running the application
- Lines 145-408: Complete API documentation for 8 endpoints:
  1. GET /health (lines 150-160)
  2. POST /action-items/extract (lines 164-187)
  3. POST /action-items/extract-llm (lines 191-216)
  4. GET /action-items (lines 220-246)
  5. POST /action-items/{id}/done (lines 250-271)
  6. POST /notes (lines 275-294)
  7. GET /notes/{id} (lines 298-313)
  8. GET /notes (lines 317-340)
- Lines 342-360: cURL examples for all endpoints
- Lines 362-413: Testing instructions
  - Multiple test commands
  - Expected output
  - Coverage instructions
- Lines 415-458: Project structure with ASCII tree
- Lines 460-522: Configuration documentation
  - Environment variables table
  - Database schema
- Lines 524-537: Development tools section
- Lines 539-605: Troubleshooting guide (4 common issues)
- Lines 607-622: Performance notes with comparison table
- Lines 624-638: Contributing, license, acknowledgments

Key features:
✓ Emoji section headers for visual navigation
✓ Syntax-highlighted code blocks
✓ Tables for structured data (tech stack, config, performance)
✓ Realistic request/response examples
✓ Comprehensive troubleshooting
✓ Professional formatting throughout
✓ Links to /docs for interactive API exploration
```


## SUBMISSION INSTRUCTIONS
1. Hit a `Command (⌘) + F` (or `Ctrl + F`) to find any remaining `TODO`s in this file. If no results are found, congratulations – you've completed all required fields. 
2. Make sure you have all changes pushed to your remote repository for grading.
3. Submit via Gradescope. 