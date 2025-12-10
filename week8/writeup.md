# Week 8 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## Instructions

Fill out all of the `TODO`s in this file.

## Submission Details

Name: **William Li** \
SUNet ID: **willyli** \
Citations: **Bolt.new for Version 1, Claude (Cursor) for Versions 2 and 3**

This assignment took me about **4** hours to do. 


## App Concept 

Task Manager: A full-stack CRUD application for managing personal tasks and to-do items.

Main Features:
- Create tasks with title, description, and completion status
- View all tasks in a clean, organized list
- Edit existing tasks to update details
- Delete tasks with confirmation
- Mark tasks as completed/pending
- Persistent storage with database
- Input validation (title required, max length 200 characters)
- Responsive UI with modern gradient design
- Real-time updates after CRUD operations

The app demonstrates a complete end-to-end web application with frontend, backend API, and database persistence across three different technology stacks.


## Version #1 Description
```
APP DETAILS:
===============
Folder name: project-bolt
Deployed URL: https://basic-crud-app-pr3o.bolt.host
AI app generation platform: Bolt.new
Tech Stack: React 18 + TypeScript + Vite frontend, Bolt Database backend (PostgreSQL)
Persistence: Bolt Database PostgreSQL database with Row Level Security (RLS)
Frameworks/Libraries Used:
  - Frontend: React 18.3.1, TypeScript 5.5.3, Vite 5.4.2, Tailwind CSS 3.4.1
  - Icons: Lucide React 0.344.0
  - Backend: Bolt Database (Bolt Database-js 2.57.4)
  - Database: PostgreSQL with RLS policies
Code Statistics: ~517 lines of TypeScript/TSX across 5 main files

REFLECTIONS:
===============
a. Issues encountered per stack and how you resolved them: 
The main challenge was setting up proper Row Level Security (RLS) policies for the Bolt Database. Initial policies used direct auth.uid() calls which caused performance warnings - resolved by wrapping them in subqueries: (select auth.uid()). This optimization evaluates the user ID once per query instead of per row. Authentication setup required understanding Supabase's onAuthStateChange callback patterns and avoiding deadlocks by using async blocks inside callbacks rather than async callbacks directly. The Bolt Database client configuration was straightforward using environment variables. TypeScript provided excellent type safety throughout the app with proper type definitions for Task entities.

b. Prompting (e.g. what required additional guidance; what worked poorly/well): 
What worked well: Claude Code generated clean, modular component architecture with proper separation of concerns (AuthForm, TaskItem, AddTaskForm as separate components). Requesting "Supabase with RLS" produced secure database policies immediately. Specifying TypeScript resulted in fully typed code with no 'any' types. What needed refinement: Initial RLS policies needed optimization for performance (auth.uid() → select auth.uid()). An unused database index (tasks_completed_idx) was created and later removed after analyzing query patterns. The auth callback pattern required specific guidance to avoid deadlocks. Overall, Claude excelled at generating production-ready code with proper error handling, loading states, and security best practices.

c. Approximate time-to-first-run and time-to-feature metrics: 
Time to first working app: ~15 minutes (database migration, auth setup, basic UI)
Time to full CRUD feature set: ~30 minutes (all operations with validation and filtering)
Time to polished version: ~45 minutes (responsive design, hover states, inline editing)
Time for security optimization: ~10 minutes (RLS policy optimization, removing unused index)
Total development time: ~1 hour

Additional notes: Supabase's built-in authentication eliminated the need for custom JWT handling or session management. RLS policies at the database level provide security guarantees even if frontend code is bypassed. The app uses optimistic UI patterns but refetches data after mutations to ensure consistency. Migration files include detailed markdown comments explaining all schema changes and security policies for maintainability.
```

## Version #2 Description
```
APP DETAILS:
===============
Folder name: flask-task-manager
AI app generation platform: Claude (Cursor) - manual coding with AI assistance
Tech Stack: Flask (Python) + Vanilla JavaScript
Persistence: SQLite database with direct SQL queries
Frameworks/Libraries Used: Flask, flask-cors, sqlite3
Non-JS Language: Python backend (satisfies assignment requirement)

REFLECTIONS:
===============
a. Issues encountered per stack and how you resolved them: 
Flask's simplicity made it easy to set up, but required more manual SQL writing compared to Django's ORM. The main issue was ensuring proper database initialization on first run - resolved by calling init_db() at startup. CORS configuration was straightforward with flask-cors. Serving static files and templates required understanding Flask's folder structure (templates/ and static/ directories). Vanilla JavaScript required more DOM manipulation code compared to React, but kept the frontend lightweight with no build process.

b. Prompting (e.g. what required additional guidance; what worked poorly/well): 
Claude handled the Flask backend structure well, generating clean route definitions and proper error handling. What worked well: requesting RESTful API patterns, asking for validation in route handlers, specifying SQLite for simplicity. What needed guidance: ensuring proper HTTP status codes (201 for create, 204 for delete), getting the escapeHtml function for XSS prevention in vanilla JS, and structuring the CSS for a modern gradient design. AI is excellent at generating Flask boilerplate but sometimes needs reminders about security best practices.

c. Approximate time-to-first-run and time-to-feature metrics: 
Time to first working app: ~45 minutes (setting up Flask structure, routes, templates)
Time to full feature set: ~90 minutes (adding all CRUD, validation, styling)
Time to polished version: ~120 minutes (refining UI, testing edge cases)
Total development time: ~2 hours
```

## Version #3 Description
```
APP DETAILS:
===============
Folder name: django-react-task-manager
AI app generation platform: Claude (Cursor) - manual coding with AI assistance
Tech Stack: Django REST Framework (Python) + React (JavaScript)
Persistence: SQLite with Django ORM and migrations
Frameworks/Libraries Used: Django, djangorestframework, django-cors-headers, React, Axios
Non-JS Language: Python backend with Django (satisfies assignment requirement)

REFLECTIONS:
===============
a. Issues encountered per stack and how you resolved them: 
Django's convention-heavy structure required understanding settings.py configuration, URL routing patterns, and the app structure (backend/ vs tasks_api/). Main issues: ensuring CORS was properly configured with django-cors-headers middleware, understanding Django REST Framework's ViewSet pattern (different from Flask's explicit routes), and remembering to run migrations before first use. Resolved by following Django/DRF best practices for serializer validation and ViewSet organization. The React frontend was identical to the Express version but with different API URL (port 8000 vs 3001).

b. Prompting (e.g. what required additional guidance; what worked poorly/well): 
Claude excelled at generating Django boilerplate (settings.py, models, serializers, ViewSets). What worked well: asking for "Django REST Framework with ViewSets", requesting serializer validation, specifying model fields with Django field types. What needed guidance: ensuring the app was registered in INSTALLED_APPS, setting up URL routing with DefaultRouter, configuring CORS middleware in the correct order. AI sometimes generated Django 3.x patterns when Django 4.x was specified, requiring minor adjustments. Overall, Django's explicit structure makes it easier for AI to generate correct code compared to Flask's flexibility.

c. Approximate time-to-first-run and time-to-feature metrics: 
Time to first working app: ~60 minutes (Django setup, models, migrations, DRF ViewSets)
Time to full feature set: ~90 minutes (all CRUD with ViewSets, React frontend, testing)
Time to polished version: ~120 minutes (admin panel config, validation refinement, README)
Total development time: ~2 hours

Additional notes: Django provides excellent built-in admin interface at /admin for database management without extra code. The migration system makes schema changes safer than direct SQL. DRF's ViewSets reduce boilerplate significantly - one ViewSet class provides all CRUD endpoints automatically.
```
