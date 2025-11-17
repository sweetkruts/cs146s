# Task Manager - Bolt.new Version

A modern full-stack task management application built with React, TypeScript, Vite, and Supabase, generated using Bolt.new AI platform.

**Live Deployment:** https://basic-crud-app-pr3o.bolt.host

## Tech Stack

- **Frontend**: React 18.3.1, TypeScript 5.5.3, Vite 5.4.2
- **Styling**: Tailwind CSS 3.4.1
- **Icons**: Lucide React 0.344.0
- **Backend/Database**: Supabase (PostgreSQL with Row Level Security)
- **Database Client**: @supabase/supabase-js 2.57.4
- **Authentication**: Supabase Auth

## Prerequisites

- Node.js 18+ and npm
- Supabase account (for database and authentication)
- Modern web browser

## Installation & Setup

### 1. Clone and Install Dependencies

```bash
cd week8/project-bolt
npm install
```

### 2. Environment Configuration

Create a `.env` file in the project root:

```env
VITE_SUPABASE_URL=your_supabase_project_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

**To get your Supabase credentials:**
1. Go to https://supabase.com and create a free account
2. Create a new project
3. Go to Project Settings > API
4. Copy the Project URL and anon/public API key

### 3. Database Setup

The database migrations are included in `supabase/migrations/`:

**Option A: Using Supabase Dashboard (Easiest)**
1. Go to your Supabase project dashboard
2. Navigate to SQL Editor
3. Run the SQL from `supabase/migrations/20251117001349_create_tasks_table.sql`
4. Run the SQL from `supabase/migrations/20251117001948_fix_rls_performance_and_cleanup.sql`

**Option B: Using Supabase CLI**
```bash
# Install Supabase CLI
npm install -g supabase

# Initialize Supabase
supabase init

# Link to your project
supabase link --project-ref your-project-ref

# Run migrations
supabase db push
```

### 4. Run the Application

```bash
npm run dev
```

The app will be available at `http://localhost:5173`

## Features

- **Authentication**: Email/password signup and login with Supabase Auth
- **Create**: Add new tasks with title, description, and completion status
- **Read**: View all your tasks in a clean, organized list
- **Update**: Edit tasks inline with immediate feedback
- **Delete**: Remove tasks with confirmation dialog
- **Filter**: Toggle between all tasks, active tasks, and completed tasks
- **Validation**: Title required, client and server-side validation
- **Security**: Row Level Security (RLS) ensures users only see their own tasks
- **Persistence**: PostgreSQL database with automatic syncing
- **Responsive**: Mobile-friendly UI with Tailwind CSS

## Project Structure

```
project-bolt/
├── src/
│   ├── components/
│   │   ├── AuthForm.tsx       # Login/signup form
│   │   ├── TaskItem.tsx       # Individual task card
│   │   └── AddTaskForm.tsx    # Task creation form
│   ├── lib/
│   │   └── supabase.ts        # Supabase client configuration
│   ├── App.tsx                # Main application component
│   ├── main.tsx               # Application entry point
│   └── index.css              # Tailwind CSS styles
├── supabase/
│   └── migrations/            # Database schema migrations
│       ├── 20251117001349_create_tasks_table.sql
│       └── 20251117001948_fix_rls_performance_and_cleanup.sql
├── package.json
└── vite.config.ts
```

## Database Schema

### Tasks Table
```sql
CREATE TABLE tasks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  title TEXT NOT NULL CHECK (length(title) <= 200),
  description TEXT,
  completed BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Row Level Security Policies
- Users can only view their own tasks
- Users can only create tasks for themselves
- Users can only update their own tasks
- Users can only delete their own tasks

All policies are optimized with subqueries: `(SELECT auth.uid())` for performance.

## Build for Production

```bash
npm run build
```

This creates an optimized production build in the `dist/` directory.

## Deployment

This app is deployed on Bolt.new's hosting platform at:
https://basic-crud-app-pr3o.bolt.host

**To deploy elsewhere:**
- Vercel: `vercel deploy`
- Netlify: `netlify deploy`
- Any static hosting: Upload the `dist/` folder

## Environment Variables

Required environment variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_SUPABASE_URL` | Your Supabase project URL | `https://xxxxx.supabase.co` |
| `VITE_SUPABASE_ANON_KEY` | Your Supabase anonymous key | `eyJhbGci...` |

## API Endpoints

All API interactions are handled through Supabase client methods:

- `supabase.auth.signUp()` - User registration
- `supabase.auth.signInWithPassword()` - User login
- `supabase.auth.signOut()` - User logout
- `supabase.from('tasks').select()` - Fetch tasks
- `supabase.from('tasks').insert()` - Create task
- `supabase.from('tasks').update()` - Update task
- `supabase.from('tasks').delete()` - Delete task

## Known Issues & Notes

- Requires active internet connection (uses Supabase cloud)
- Authentication session persists in localStorage
- RLS policies enforce data isolation between users
- Database indexes optimized for common query patterns
- Real-time subscriptions available but not implemented in this version

## Development Notes

This version was generated using **Bolt.new**, an AI-powered development platform:

**Advantages:**
- Rapid prototyping (working app in minutes)
- Modern stack by default (React, TypeScript, Vite)
- Automatic deployment and hosting
- Production-ready patterns (TypeScript, proper error handling)
- Security best practices (RLS, input validation)

**Generated Code Statistics:**
- ~517 lines of TypeScript/TSX
- 5 main component files
- 2 database migration files
- Full type safety with TypeScript
- Zero 'any' types

**Bolt.new Prompting Tips:**
1. Start with clear data model description
2. Specify validation rules explicitly
3. Request security features (RLS, authentication)
4. Iterate on UI/UX with follow-up prompts
5. Ask for TypeScript for better code quality

## Security Features

- **Row Level Security**: Database-level access control
- **Authentication**: Supabase Auth with secure session management
- **Input Validation**: Client-side and database constraints
- **SQL Injection Prevention**: Parameterized queries via Supabase client
- **XSS Prevention**: React's built-in escaping
- **HTTPS**: All communication encrypted (production)

## Comparison with Other Stacks

See the main `writeup.md` for detailed comparison with Flask and Django implementations.

**Key Differences:**
- **Bolt.new (this)**: Fastest development, modern stack, cloud-native
- **Flask**: Simplest backend, manual SQL, lightweight
- **Django**: Most mature, ORM + migrations, built-in admin

## Support & Resources

- [Supabase Documentation](https://supabase.com/docs)
- [Vite Documentation](https://vitejs.dev/)
- [React Documentation](https://react.dev/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)
- [Bolt.new Documentation](https://support.bolt.new/)

## License

MIT - Educational project for CS146 Stanford

