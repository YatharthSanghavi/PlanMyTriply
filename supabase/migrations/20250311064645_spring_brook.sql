/*
  # Remove cover image from travel guides

  1. Changes
    - Remove cover_image column from travel_guides table since we don't want to store images
    - Add default_bg_color column to provide a fallback background color for guides
    - Add icon column to store an icon identifier for the guide

  2. Security
    - Maintain existing RLS policies
*/

-- Add new columns first
ALTER TABLE travel_guides 
ADD COLUMN IF NOT EXISTS default_bg_color text NOT NULL DEFAULT '#4F46E5',
ADD COLUMN IF NOT EXISTS icon text NOT NULL DEFAULT 'compass';

-- Remove cover_image column
DO $$ 
BEGIN
  IF EXISTS (
    SELECT 1 FROM information_schema.columns 
    WHERE table_name = 'travel_guides' AND column_name = 'cover_image'
  ) THEN
    ALTER TABLE travel_guides DROP COLUMN cover_image;
  END IF;
END $$;