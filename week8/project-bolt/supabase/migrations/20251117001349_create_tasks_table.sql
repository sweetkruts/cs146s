/*
  # Create tasks table for task management app

  ## Overview
  This migration creates a tasks table for a task management application with full CRUD capabilities.

  ## New Tables
  - `tasks`
    - `id` (uuid, primary key) - Unique identifier for each task
    - `user_id` (uuid) - Reference to the authenticated user who owns the task
    - `title` (text, required) - The task title/name
    - `description` (text) - Optional detailed description of the task
    - `completed` (boolean, default false) - Task completion status
    - `created_at` (timestamptz) - Timestamp when task was created
    - `updated_at` (timestamptz) - Timestamp when task was last updated

  ## Security
  - Enable Row Level Security (RLS) on tasks table
  - Add policy for authenticated users to view their own tasks
  - Add policy for authenticated users to insert their own tasks
  - Add policy for authenticated users to update their own tasks
  - Add policy for authenticated users to delete their own tasks

  ## Important Notes
  1. All tasks are user-specific and isolated through RLS
  2. Users can only access, modify, and delete their own tasks
  3. The user_id is automatically validated against the authenticated user
*/

CREATE TABLE IF NOT EXISTS tasks (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL,
  title text NOT NULL,
  description text DEFAULT '',
  completed boolean DEFAULT false,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own tasks"
  ON tasks FOR SELECT
  TO authenticated
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own tasks"
  ON tasks FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own tasks"
  ON tasks FOR UPDATE
  TO authenticated
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own tasks"
  ON tasks FOR DELETE
  TO authenticated
  USING (auth.uid() = user_id);

CREATE INDEX IF NOT EXISTS tasks_user_id_idx ON tasks(user_id);
CREATE INDEX IF NOT EXISTS tasks_completed_idx ON tasks(completed);