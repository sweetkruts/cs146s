# Task Manager - Flask + Vanilla JS Version

A simple task management web application built with Flask (Python backend) and Vanilla JavaScript (frontend).

## Tech Stack

- **Backend**: Flask (Python 3.8+)
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Database**: SQLite
- **Libraries**: flask-cors for CORS support

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation & Setup

1. Navigate to the project directory:
```bash
cd week8/flask-task-manager
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

The database will be automatically created on first run.

## Features

- **Create**: Add new tasks with title, description, and completion status
- **Read**: View all tasks in a list
- **Update**: Edit existing tasks
- **Delete**: Remove tasks with confirmation
- **Validation**: Client and server-side validation (title required, max 200 chars)
- **Persistence**: SQLite database storage
- **Responsive UI**: Modern, gradient design with hover effects

## API Endpoints

- `GET /api/tasks` - Get all tasks
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/<id>` - Get a specific task
- `PUT /api/tasks/<id>` - Update a task
- `DELETE /api/tasks/<id>` - Delete a task

## Environment Configuration

No environment variables required. The application uses:
- Port: 5000
- Database: tasks.db (created automatically in project root)

## Known Issues & Notes

- Database file is created in the project root directory
- No authentication/authorization implemented
- CORS is enabled for all origins (development only)
- No migration system - database schema is created on startup

## Development Notes

This version was built manually (not using AI generation platforms) to demonstrate:
- Traditional Python web framework (Flask)
- Server-side rendering with Jinja2 templates
- Vanilla JavaScript without frameworks
- Simple file-based SQLite persistence

