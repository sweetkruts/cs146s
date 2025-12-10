/*
  # Fix RLS Performance Issues and Remove Unused Index

  ## Overview
  This migration optimizes the RLS policies on the tasks table by using
  (select auth.uid()) instead of auth.uid() directly, which prevents
  re-evaluation for each row and significantly improves query performance at scale.
  It also removes the unused tasks_completed_idx index.

  ## Changes Made
  1. Drop and recreate all four RLS policies with optimized auth function calls:
     - "Users can view own tasks" - SELECT policy
     - "Users can insert own tasks" - INSERT policy
     - "Users can update own tasks" - UPDATE policy
     - "Users can delete own tasks" - DELETE policy

  2. Remove unused index:
     - Drop tasks_completed_idx (not being used by queries)

  ## Performance Impact
  - RLS policies will now evaluate auth.uid() once per query instead of once per row
  - This provides significant performance improvements as the number of tasks grows
  - Reduced index overhead by removing unused index

  ## Security
  - All policies maintain the same security guarantees
  - Users can still only access, modify, and delete their own tasks
  - No changes to the security model, only performance optimization
*/

DROP POLICY IF EXISTS "Users can view own tasks" ON tasks;
DROP POLICY IF EXISTS "Users can insert own tasks" ON tasks;
DROP POLICY IF EXISTS "Users can update own tasks" ON tasks;
DROP POLICY IF EXISTS "Users can delete own tasks" ON tasks;

CREATE POLICY "Users can view own tasks"
  ON tasks FOR SELECT
  TO authenticated
  USING ((select auth.uid()) = user_id);

CREATE POLICY "Users can insert own tasks"
  ON tasks FOR INSERT
  TO authenticated
  WITH CHECK ((select auth.uid()) = user_id);

CREATE POLICY "Users can update own tasks"
  ON tasks FOR UPDATE
  TO authenticated
  USING ((select auth.uid()) = user_id)
  WITH CHECK ((select auth.uid()) = user_id);

CREATE POLICY "Users can delete own tasks"
  ON tasks FOR DELETE
  TO authenticated
  USING ((select auth.uid()) = user_id);

DROP INDEX IF EXISTS tasks_completed_idx;