/*
  # Update Travel Plans Policies

  1. Changes
    - Remove authentication requirement for inserting plans
    - Allow public access for all operations

  2. Security
    - Enable RLS on travel_plans table
    - Add policy for public access to all operations
*/

-- Drop existing policies if they exist
DROP POLICY IF EXISTS "Allow public read access" ON travel_plans;
DROP POLICY IF EXISTS "Allow authenticated users to create plans" ON travel_plans;

-- Create new public access policy
CREATE POLICY "Allow public access"
  ON travel_plans
  FOR ALL
  TO public
  USING (true)
  WITH CHECK (true);