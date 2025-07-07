/*
  # Create hotel searches table

  1. New Tables
    - `hotel_searches`
      - `id` (uuid, primary key): Unique identifier for each search
      - `location` (text, required): Search location
      - `check_in` (date, required): Check-in date
      - `check_out` (date, required): Check-out date
      - `guests` (integer, required): Number of guests
      - `preferences` (text): Special preferences
      - `budget` (text, required): Budget level
      - `recommendations` (text, required): AI-generated recommendations
      - `search_results` (jsonb): Raw search results
      - `created_at` (timestamptz): Creation timestamp

  2. Security
    - Enable RLS on `hotel_searches` table
    - Add policy for public access to all operations
*/

-- Create hotel searches table
CREATE TABLE IF NOT EXISTS hotel_searches (
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

-- Drop existing policy if it exists
DO $$ 
BEGIN
    IF EXISTS (
        SELECT 1 FROM pg_policies 
        WHERE tablename = 'hotel_searches' 
        AND policyname = 'Allow public access'
    ) THEN
        DROP POLICY IF EXISTS "Allow public access" ON hotel_searches;
    END IF;
END $$;

-- Create policy for public access
CREATE POLICY "Allow public access"
    ON hotel_searches
    FOR ALL
    TO public
    USING (true)
    WITH CHECK (true);

-- Create index for faster retrieval
CREATE INDEX IF NOT EXISTS hotel_searches_created_at_idx ON hotel_searches (created_at DESC);