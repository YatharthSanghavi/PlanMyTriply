/*
  # Travel Planner Schema

  1. New Tables
    - `travel_plans`
      - `id` (uuid, primary key)
      - `destination` (text)
      - `days` (integer)
      - `people` (integer) 
      - `accommodation` (text)
      - `activities` (text)
      - `interests` (text)
      - `budget` (text)
      - `content` (text)
      - `created_at` (timestamptz)
      - `sources` (jsonb)

  2. Security
    - Enable RLS on `travel_plans` table
    - Add policy for public read access
    - Add policy for authenticated users to create plans
*/

-- Create travel plans table
CREATE TABLE IF NOT EXISTS travel_plans (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  destination text NOT NULL,
  days integer NOT NULL,
  people integer NOT NULL,
  accommodation text NOT NULL,
  activities text NOT NULL,
  interests text,
  budget text NOT NULL,
  content text NOT NULL,
  sources jsonb,
  created_at timestamptz DEFAULT now()
);

-- Enable Row Level Security
ALTER TABLE travel_plans ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Allow public read access"
  ON travel_plans
  FOR SELECT
  TO public
  USING (true);

CREATE POLICY "Allow authenticated users to create plans"
  ON travel_plans
  FOR INSERT
  TO authenticated
  WITH CHECK (true);