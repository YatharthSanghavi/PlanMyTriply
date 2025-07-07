/*
  # Create travel guides table

  1. New Tables
    - `travel_guides`
      - `id` (uuid, primary key): Unique identifier for each guide
      - `title` (text, not null): Guide title
      - `content` (text, not null): Main content of the guide
      - `excerpt` (text, not null): Brief summary for preview
      - `cover_image` (text, not null): URL to the guide's cover image
      - `author` (text, not null): Guide author
      - `category` (text, not null): Guide category for filtering
      - `tags` (text[], nullable): Array of tags for categorization
      - `created_at` (timestamptz): Creation timestamp
      - `updated_at` (timestamptz): Last update timestamp

  2. Security
    - Enable RLS on `travel_guides` table
    - Add policy for public read access
    - Add policy for authenticated users to create/update/delete

  3. Triggers
    - Add trigger to automatically update updated_at timestamp
*/

-- Create travel guides table
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

-- Allow public read access
CREATE POLICY "Allow public read access" 
    ON travel_guides
    FOR SELECT 
    TO public
    USING (true);

-- Allow authenticated users to create/update/delete
CREATE POLICY "Allow authenticated users full access" 
    ON travel_guides
    FOR ALL 
    TO authenticated
    USING (true)
    WITH CHECK (true);

-- Function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger to automatically update the updated_at column
CREATE TRIGGER update_travel_guides_updated_at
    BEFORE UPDATE ON travel_guides
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS travel_guides_category_idx ON travel_guides (category);
CREATE INDEX IF NOT EXISTS travel_guides_created_at_idx ON travel_guides (created_at DESC);