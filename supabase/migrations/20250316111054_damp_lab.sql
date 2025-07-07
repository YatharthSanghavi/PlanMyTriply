/*
  # Update hotel searches table for markdown content

  1. Changes
    - Add markdown_content column to store formatted content
    - Update recommendations column to store raw markdown
    - Add index for better search performance

  2. Security
    - Maintain existing RLS policies
*/

-- Add markdown_content column
ALTER TABLE hotel_searches
ADD COLUMN IF NOT EXISTS markdown_content text;

-- Create index for faster searches
CREATE INDEX IF NOT EXISTS hotel_searches_location_idx ON hotel_searches (location);