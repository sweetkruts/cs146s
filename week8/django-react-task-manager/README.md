# Task Manager - Django + React Version

A full-stack task management application built with Django REST Framework (Python backend) and React (frontend).

## Tech Stack

- **Backend**: Django 4.2, Django REST Framework
- **Frontend**: React 18, Axios
- **Database**: SQLite
- **Additional**: django-cors-headers, ViewSets, Serializers

## Prerequisites

- Python 3.8+
- Node.js 14+ and npm
- pip (Python package manager)

## Installation & Setup

### Backend Setup

1. Navigate to the backend directory:
```bash
cd week8/django-react-task-manager/backend
```

2. Create and activate a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. (Optional) Create a superuser for Django admin:
```bash
python manage.py createsuperuser
```

6. Start the Django development server:
```bash
python manage.py runserver
```

Backend will run on `http://localhost:8000`

### Frontend Setup

1. Open a new terminal and navigate to the frontend directory:
```bash
cd week8/django-react-task-manager/frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the React development server:
```bash
npm start
```

Frontend will run on `http://localhost:3000`

## Running the Application

1. Start the Django backend server first (port 8000)
2. Start the React frontend development server (port 3000)
3. Open your browser to `http://localhost:3000`

## Features

- **Create**: Add new tasks with title, description, and completion status
- **Read**: View all tasks ordered by creation date (newest first)
- **Update**: Edit existing tasks with form validation
- **Delete**: Remove tasks with confirmation dialog
- **Validation**: Server-side validation with Django REST Framework serializers
- **Persistence**: SQLite database with Django ORM
- **Admin Interface**: Django admin panel at `/admin` for database management
- **REST API**: Full RESTful API with ViewSets and Routers

## API Endpoints

Django REST Framework provides the following endpoints:

- `GET /api/tasks/` - List all tasks
- `POST /api/tasks/` - Create a new task
- `GET /api/tasks/<id>/` - Retrieve a specific task
- `PUT /api/tasks/<id>/` - Update a task
- `PATCH /api/tasks/<id>/` - Partial update a task
- `DELETE /api/tasks/<id>/` - Delete a task

API browsable interface available at `http://localhost:8000/api/`

## Project Structure

```
django-react-task-manager/
├── backend/
│   ├── backend/
│   │   ├── settings.py      # Django settings
│   │   ├── urls.py          # URL configuration
│   │   └── wsgi.py          # WSGI configuration
│   ├── tasks_api/
│   │   ├── models.py        # Task model
│   │   ├── serializers.py   # DRF serializers
│   │   ├── views.py         # ViewSet for CRUD operations
│   │   ├── urls.py          # API routing
│   │   └── admin.py         # Admin configuration
│   ├── manage.py            # Django management script
│   └── requirements.txt     # Python dependencies
└── frontend/
    ├── public/
    │   └── index.html       # HTML template
    ├── src/
    │   ├── components/
    │   │   ├── TaskForm.js  # Task creation/edit form
    │   │   └── TaskList.js  # Task list display
    │   ├── App.js           # Main application component
    │   ├── App.css          # Application styles
    │   └── index.js         # React entry point
    └── package.json         # Frontend dependencies
```

## Environment Configuration

### Backend
- Port: 8000 (default)
- Database: db.sqlite3 (created automatically in backend directory)
- Debug mode: Enabled (set DEBUG=False in production)
- CORS: Enabled for all origins (change for production)

### Frontend
- Port: 3000 (default)
- API Proxy: Configured to proxy /api requests to http://localhost:8000

## Admin Panel

Access Django admin at `http://localhost:8000/admin` to:
- View and manage tasks directly
- Filter tasks by completion status and creation date
- Search tasks by title and description

## Known Issues & Notes

- Database migrations are required before first run
- CORS is enabled for all origins (development only - configure for production)
- No authentication/authorization implemented
- SECRET_KEY is hard-coded (change for production)
- React development server proxies API requests to Django backend

## Development Notes

This version demonstrates:
- **Django REST Framework** - Enterprise-grade Python web framework with DRF
- **Model-View-Serializer architecture** - Clean separation of concerns
- **ORM-based persistence** - Django ORM with migrations
- **Serializer validation** - Server-side validation with DRF
- **ViewSets and Routers** - Automatic RESTful routing
- **Admin interface** - Built-in database management UI
- **Python type safety** - Model field definitions with Django

## Advantages of Django + React

- **Mature ecosystem**: Django is battle-tested for production applications
- **Built-in admin**: Instant database management interface
- **ORM migrations**: Schema changes tracked and versioned
- **Security features**: CSRF protection, SQL injection prevention, XSS protection
- **Serializer validation**: Declarative validation with DRF serializers
- **ViewSets**: Less boilerplate code for standard CRUD operations
- **Python backend**: Ideal for data science, ML integration, complex business logic

