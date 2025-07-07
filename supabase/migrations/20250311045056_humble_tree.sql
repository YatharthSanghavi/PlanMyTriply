/*
  # Create travel guides table

  1. New Tables
    - `travel_guides`
      - `id` (uuid, primary key)
      - `title` (text, required)
      - `content` (text, required)
      - `excerpt` (text, required)
      - `cover_image` (text, required)
      - `author` (text, required)
      - `category` (text, required)
      - `tags` (text[], optional)
      - `created_at` (timestamptz, default now())
      - `updated_at` (timestamptz, default now())

  2. Security
    - Enable RLS on `travel_guides` table
    - Add policy for public access to all operations
    
  3. Triggers
    - Add updated_at trigger to automatically update the timestamp
*/

-- Create travel guides table if it doesn't exist
CREATE TABLE IF NOT EXISTS travel_guides (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    title text NOT NULL,
    content text NOT NULL,
    excerpt text NOT NULL,
    cover_image text NOT NULL,
    author text NOT NULL,
    category text NOT NULL,
    tags text[],
    created_at timestamptz DEFAULT now(),
    updated_at timestamptz DEFAULT now()
);

-- Enable RLS
ALTER TABLE travel_guides ENABLE ROW LEVEL SECURITY;

-- Drop existing policy if it exists
DROP POLICY IF EXISTS "Allow public access" ON travel_guides;

-- Create policy for public access
CREATE POLICY "Allow public access"
    ON travel_guides
    FOR ALL
    TO public
    USING (true)
    WITH CHECK (true);

-- Create or replace the updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Drop trigger if exists and create it
DROP TRIGGER IF EXISTS update_travel_guides_updated_at ON travel_guides;
CREATE TRIGGER update_travel_guides_updated_at
    BEFORE UPDATE ON travel_guides
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();