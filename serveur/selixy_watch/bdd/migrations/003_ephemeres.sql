ALTER TABLE comptes ADD COLUMN ephemere boolean NOT NULL DEFAULT false;
CREATE INDEX comptes_ephemeres ON comptes (id) WHERE ephemere;
