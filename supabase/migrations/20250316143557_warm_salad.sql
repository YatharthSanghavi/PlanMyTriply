/*
  # Update hotel searches table

  1. Changes
    - Make check_in and check_out dates optional
    - Add markdown_content column if not exists
    - Add location index if not exists

  2. Security
    - Maintain existing RLS policies
*/

-- Make check_in and check_out nullable
ALTER TABLE hotel_searches 
ALTER COLUMN check_in DROP NOT NULL,
ALTER COLUMN check_out DROP NOT NULL;

-- Add markdown_content column if not exists
DO $$ 
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns 
    WHERE table_name = 'hotel_searches' AND column_name = 'markdown_content'
  ) THEN
    ALTER TABLE hotel_searches ADD COLUMN markdown_content text;
  END IF;
END $$;

-- Create index for faster searches if not exists
DO $$ 
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_indexes 
    WHERE tablename = 'hotel_searches' AND indexname = 'hotel_searches_location_idx'
  ) THEN
    CREATE INDEX hotel_searches_location_idx ON hotel_searches (location);
  END IF;
END $$;