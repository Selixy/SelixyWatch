CREATE TABLE invitation_noeuds (
    invitation_id text NOT NULL REFERENCES invitations (id) ON DELETE CASCADE,
    noeud_id text NOT NULL REFERENCES noeuds (id) ON DELETE CASCADE,
    PRIMARY KEY (invitation_id, noeud_id)
);
CREATE INDEX invitation_noeuds_noeud ON invitation_noeuds (noeud_id);

INSERT INTO invitation_noeuds (invitation_id, noeud_id) SELECT id, noeud_id FROM invitations;
UPDATE invitations SET role = 'editeur';
ALTER TABLE invitations DROP COLUMN noeud_id;

ALTER TABLE comptes ADD COLUMN admin boolean NOT NULL DEFAULT false;
