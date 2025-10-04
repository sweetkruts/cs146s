# Action Item Extractor

A FastAPI-based web application that automatically extracts actionable tasks from free-form text notes. Features both heuristic-based and LLM-powered extraction methods to identify and organize action items from meeting notes, project plans, or any text input.

## 🎯 Overview

This application helps users quickly identify and manage action items from unstructured notes. It provides:

- **Dual Extraction Methods**: Choose between fast heuristic patterns or semantic LLM-based extraction
- **Note Management**: Save and retrieve notes for future reference
- **Interactive UI**: Simple web interface for extracting and managing action items
- **RESTful API**: Well-documented endpoints for programmatic access
- **Persistent Storage**: SQLite database for notes and action items

## ✨ Features

### Extraction Methods

1. **Heuristic Extraction** (Fast)
   - Pattern-based recognition of bullet points, numbered lists
   - Keyword detection (TODO, action, next, etc.)
   - Checkbox markers (`[ ]`, `[x]`, `[todo]`)
   - Imperative verb detection

2. **LLM Extraction** (Accurate)
   - Semantic understanding using Ollama
   - Context-aware extraction
   - Better handling of complex narrative text
   - Structured JSON output

### Core Functionality

- ✅ Extract action items from free-form text
- ✅ Save notes with associated action items
- ✅ Mark items as complete/incomplete
- ✅ List all saved notes with timestamps
- ✅ RESTful API with OpenAPI documentation
- ✅ Type-safe with Pydantic schemas

## 🛠 Tech Stack

**Backend:**
- FastAPI 0.111+ (Web framework)
- SQLite (Database)
- Pydantic 2.0+ (Data validation)
- Ollama (LLM integration)
- Python 3.10+

**Frontend:**
- Vanilla JavaScript
- HTML5/CSS3
- Fetch API

**Development:**
- Poetry (Dependency management)
- Pytest (Testing framework)
- Black & Ruff (Code formatting/linting)

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10 or higher**
  ```bash
  python --version
  ```

- **Poetry** (Dependency management)
  ```bash
  curl -sSL https://install.python-poetry.org | python3 -
  ```

- **Ollama** (For LLM-based extraction)
  ```bash
  # macOS
  brew install ollama
  
  # Or download from: https://ollama.com/download
  ```

- **Ollama Model** (Required for LLM extraction)
  ```bash
  ollama pull llama3.1:8b
  # Or use: ollama pull mistral-nemo:12b
  ```

## 🚀 Setup & Installation

### 1. Clone the Repository

```bash
cd /path/to/modern-software-dev-assignments/week2
```

### 2. Install Dependencies

```bash
poetry install
```

This will create a virtual environment and install all required packages including:
- FastAPI, Uvicorn, SQLAlchemy
- Ollama Python client
- Pytest and development tools

### 3. Verify Installation

```bash
# Check that dependencies are installed
poetry run python -c "import fastapi; print('✓ FastAPI installed')"
poetry run python -c "import ollama; print('✓ Ollama client installed')"

# Check Ollama is running
ollama list
```

## 🏃 Running the Application

### Start the Development Server

```bash
poetry run uvicorn week2.app.main:app --reload
```

**Expected output:**
```
INFO:     Starting Action Item Extractor in development mode
INFO:     Database initialized successfully
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Access the Application

- **Web Interface**: http://127.0.0.1:8000/
- **API Documentation**: http://127.0.0.1:8000/docs
- **Alternative API Docs**: http://127.0.0.1:8000/redoc
- **Health Check**: http://127.0.0.1:8000/health

### Using the Web Interface

1. **Enter Notes**: Paste or type your notes in the textarea
2. **Choose Method**: 
   - Click **"Extract (Heuristic)"** for fast pattern-based extraction
   - Click **"Extract (LLM)"** for AI-powered semantic extraction
3. **Review Items**: Extracted items appear as interactive checkboxes
4. **Mark Complete**: Check boxes to mark items as done
5. **View History**: Click **"List Notes"** to see all saved notes

## 📚 API Documentation

### Base URL
```
http://127.0.0.1:8000
```

### Endpoints

#### 1. Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "app_name": "Action Item Extractor",
  "environment": "development"
}
```

---

#### 2. Extract Action Items (Heuristic)
```http
POST /action-items/extract
```

**Request Body:**
```json
{
  "text": "Meeting notes:\n- [ ] Set up database\n- Implement API\nTODO: Write tests",
  "save_note": true
}
```

**Response:**
```json
{
  "note_id": 1,
  "items": [
    {"id": 1, "text": "Set up database"},
    {"id": 2, "text": "Implement API"},
    {"id": 3, "text": "Write tests"}
  ]
}
```

---

#### 3. Extract Action Items (LLM)
```http
POST /action-items/extract-llm
```

Uses Ollama for semantic extraction. Better at understanding context and complex text.

**Request Body:**
```json
{
  "text": "We should really get around to implementing user authentication. Also need to write comprehensive tests and deploy to production.",
  "save_note": true
}
```

**Response:**
```json
{
  "note_id": 2,
  "items": [
    {"id": 4, "text": "Implement user authentication"},
    {"id": 5, "text": "Write comprehensive tests"},
    {"id": 6, "text": "Deploy to production"}
  ]
}
```

---

#### 4. List Action Items
```http
GET /action-items?note_id={optional}
```

**Query Parameters:**
- `note_id` (optional): Filter by specific note

**Response:**
```json
[
  {
    "id": 1,
    "note_id": 1,
    "text": "Set up database",
    "done": false,
    "created_at": "2024-10-04 12:00:00"
  },
  {
    "id": 2,
    "note_id": 1,
    "text": "Implement API",
    "done": true,
    "created_at": "2024-10-04 12:00:00"
  }
]
```

---

#### 5. Mark Action Item Complete
```http
POST /action-items/{action_item_id}/done
```

**Request Body:**
```json
{
  "done": true
}
```

**Response:**
```json
{
  "id": 1,
  "done": true
}
```

---

#### 6. Create Note
```http
POST /notes
```

**Request Body:**
```json
{
  "content": "Project meeting notes from today's standup"
}
```

**Response:**
```json
{
  "id": 1,
  "content": "Project meeting notes from today's standup",
  "created_at": "2024-10-04 12:00:00"
}
```

---

#### 7. Get Single Note
```http
GET /notes/{note_id}
```

**Response:**
```json
{
  "id": 1,
  "content": "Project meeting notes from today's standup",
  "created_at": "2024-10-04 12:00:00"
}
```

---

#### 8. List All Notes
```http
GET /notes
```

**Response:**
```json
[
  {
    "id": 2,
    "content": "Latest meeting notes",
    "created_at": "2024-10-04 14:30:00"
  },
  {
    "id": 1,
    "content": "Earlier notes",
    "created_at": "2024-10-04 12:00:00"
  }
]
```

### API Examples with cURL

```bash
# Extract with heuristics
curl -X POST http://127.0.0.1:8000/action-items/extract \
  -H "Content-Type: application/json" \
  -d '{"text": "- [ ] Task 1\n- Task 2", "save_note": true}'

# Extract with LLM
curl -X POST http://127.0.0.1:8000/action-items/extract-llm \
  -H "Content-Type: application/json" \
  -d '{"text": "Need to implement auth and write tests", "save_note": true}'

# List all notes
curl http://127.0.0.1:8000/notes

# Mark item as done
curl -X POST http://127.0.0.1:8000/action-items/1/done \
  -H "Content-Type: application/json" \
  -d '{"done": true}'
```

## 🧪 Testing

### Run All Tests

```bash
poetry run pytest
```

### Run Tests with Verbose Output

```bash
poetry run pytest -v
```

### Run Specific Test File

```bash
poetry run pytest week2/tests/test_extract.py -v
```

### Run Specific Test

```bash
poetry run pytest week2/tests/test_extract.py::test_llm_extract_bullet_list -v
```

### Test Coverage

```bash
poetry run pytest --cov=week2.app --cov-report=html
```

### Expected Test Output

```
============================= test session starts ==============================
week2/tests/test_extract.py::test_extract_bullets_and_checkboxes PASSED  [ 10%]
week2/tests/test_extract.py::test_llm_extract_bullet_list PASSED         [ 20%]
week2/tests/test_extract.py::test_llm_extract_keyword_prefixed PASSED    [ 30%]
week2/tests/test_extract.py::test_llm_extract_empty_input PASSED         [ 40%]
week2/tests/test_extract.py::test_llm_extract_no_action_items PASSED     [ 50%]
week2/tests/test_extract.py::test_llm_extract_mixed_format PASSED        [ 60%]
week2/tests/test_extract.py::test_llm_extract_numbered_list PASSED       [ 70%]
week2/tests/test_extract.py::test_llm_extract_imperative_sentences PASSED [ 80%]
week2/tests/test_extract.py::test_llm_extract_deduplication PASSED       [ 90%]
week2/tests/test_extract.py::test_llm_extract_checkbox_markers PASSED    [100%]

============================== 10 passed in 5.40s ===============================
```

## 📁 Project Structure

```
week2/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application & lifecycle
│   ├── config.py            # Configuration management
│   ├── db.py                # Database layer with error handling
│   ├── schemas.py           # Pydantic models for API contracts
│   ├── routers/
│   │   ├── notes.py         # Notes endpoints
│   │   └── action_items.py  # Action items endpoints
│   └── services/
│       └── extract.py       # Extraction logic (heuristic & LLM)
├── frontend/
│   └── index.html           # Web interface
├── tests/
│   └── test_extract.py      # Unit tests
├── data/
│   └── app.db               # SQLite database (created at runtime)
├── pyproject.toml           # Poetry dependencies
└── README.md                # This file
```

### Key Components

**`main.py`**: Application entry point with lifespan management, error handlers, and route registration

**`config.py`**: Environment-based configuration with sensible defaults

**`db.py`**: Database layer with connection pooling, error handling, and custom exceptions

**`schemas.py`**: Type-safe request/response models using Pydantic

**`extract.py`**: 
- `extract_action_items()`: Heuristic-based extraction
- `extract_action_items_llm()`: LLM-based extraction with Ollama

## ⚙️ Configuration

### Environment Variables

The application can be configured via environment variables with the `APP_` prefix:

```bash
# Application Settings
export APP_NAME="Action Item Extractor"
export APP_DEBUG=false
export APP_ENVIRONMENT=development

# Database Settings
export APP_DATABASE_PATH=/custom/path/app.db

# LLM Settings
export APP_OLLAMA_MODEL=llama3.1:8b
export APP_OLLAMA_TEMPERATURE=0.1

# API Settings
export APP_CORS_ORIGINS=*
```

### Configuration Defaults

| Setting | Default | Description |
|---------|---------|-------------|
| `APP_NAME` | "Action Item Extractor" | Application name |
| `APP_DEBUG` | false | Debug mode |
| `APP_ENVIRONMENT` | development | Environment (dev/prod) |
| `APP_DATABASE_PATH` | week2/data/app.db | Database file path |
| `APP_OLLAMA_MODEL` | llama3.1:8b | Ollama model to use |
| `APP_OLLAMA_TEMPERATURE` | 0.1 | LLM temperature (0-1) |

### Database

The application uses SQLite with the following schema:

**`notes` table:**
- `id` (INTEGER PRIMARY KEY)
- `content` (TEXT)
- `created_at` (TEXT)

**`action_items` table:**
- `id` (INTEGER PRIMARY KEY)
- `note_id` (INTEGER, FOREIGN KEY)
- `text` (TEXT)
- `done` (INTEGER, 0 or 1)
- `created_at` (TEXT)

Database is automatically initialized on application startup.

## 🔧 Development

### Code Formatting

```bash
# Format code with Black
poetry run black week2/

# Lint with Ruff
poetry run ruff check week2/
```

### Pre-commit Hooks

```bash
poetry run pre-commit install
poetry run pre-commit run --all-files
```

### Interactive API Documentation

FastAPI provides automatic interactive documentation:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

Try out endpoints directly from the browser!

## 🐛 Troubleshooting

### Issue: Ollama model not found

**Error**: `model 'llama3.1:8b' not found`

**Solution**:
```bash
# Check available models
ollama list

# Pull the model
ollama pull llama3.1:8b

# Verify Ollama is running
ollama serve
```

### Issue: Port already in use

**Error**: `Address already in use`

**Solution**:
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process (replace PID)
kill -9 <PID>

# Or use a different port
poetry run uvicorn week2.app.main:app --port 8001
```

### Issue: Import errors

**Error**: `ModuleNotFoundError`

**Solution**:
```bash
# Reinstall dependencies
poetry install

# Activate virtual environment
poetry shell

# Verify installation
poetry run python -c "import fastapi; import ollama; print('OK')"
```

### Issue: Database locked

**Error**: `database is locked`

**Solution**:
```bash
# Stop all running instances
pkill -f "uvicorn week2.app.main:app"

# Remove database file (WARNING: deletes all data)
rm week2/data/app.db

# Restart server (creates fresh database)
poetry run uvicorn week2.app.main:app
```

## 📊 Performance Notes

### Extraction Method Comparison

| Method | Speed | Accuracy | Use Case |
|--------|-------|----------|----------|
| **Heuristic** | ~100ms | Good for structured text | Bullet lists, formatted notes |
| **LLM** | ~2-5s | Excellent | Complex narrative text, meeting transcripts |

### Recommendations

- **Use Heuristic** when: Text has clear formatting (bullets, numbers, keywords)
- **Use LLM** when: Text is conversational or lacks clear structure
- **Batch Processing**: For multiple notes, consider async processing

## 🤝 Contributing

This project is part of a course assignment. For questions or issues:

1. Check the [assignment documentation](assignment.md)
2. Review the [refactoring summary](REFACTORING_SUMMARY.md)
3. See [TODO 4 summary](TODO4_SUMMARY.md) for recent changes

## 📝 License

This project is developed for educational purposes as part of CS146S coursework.

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- Ollama for local LLM inference
- The CS146S teaching team

---

**Built with ❤️ using FastAPI, Ollama, and modern Python practices.**

For more details, see the [API documentation](http://127.0.0.1:8000/docs) when running the server.

