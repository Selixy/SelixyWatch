ALTER TABLE medias ADD COLUMN genre text NOT NULL DEFAULT 'video' CHECK (genre IN ('video', 'audio'));
ALTER TABLE medias ALTER COLUMN duree TYPE double precision;
ALTER TABLE invitations ADD COLUMN id text UNIQUE;
UPDATE invitations SET id = substr(jeton_hash, 1, 12) WHERE id IS NULL;
ALTER TABLE invitations ALTER COLUMN id SET NOT NULL;
