/*
  # Fix hotel searches table

  1. Changes
    - Drop existing table if exists
    - Recreate table with proper constraints
    - Enable RLS
    - Add policy for public access

  2. Security
    - Enable RLS
    - Add policy for public access to all operations
*/

-- Drop existing table and policies
DROP TABLE IF EXISTS hotel_searches;

-- Create hotel searches table
CREATE TABLE hotel_searches (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    location text NOT NULL,
    check_in date NOT NULL,
    check_out date NOT NULL,
    guests integer NOT NULL,
    preferences text,
    budget text NOT NULL,
    recommendations text NOT NULL,
    search_results jsonb,
    created_at timestamptz DEFAULT now()
);

-- Enable Row Level Security
ALTER TABLE hotel_searches ENABLE ROW LEVEL SECURITY;

-- Create policy for public access
CREATE POLICY "Allow public access"
    ON hotel_searches
    FOR ALL
    TO public
    USING (true)
    WITH CHECK (true);

-- Create index for faster retrieval
CREATE INDEX IF NOT EXISTS hotel_searches_created_at_idx ON hotel_searches (created_at DESC);