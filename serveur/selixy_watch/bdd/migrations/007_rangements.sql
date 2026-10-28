CREATE TABLE rangements (
    compte_id text NOT NULL REFERENCES comptes (id) ON DELETE CASCADE,
    noeud_id text NOT NULL REFERENCES noeuds (id) ON DELETE CASCADE,
    parent_id text REFERENCES noeuds (id) ON DELETE SET NULL,
    nom text,
    rang integer NOT NULL DEFAULT 0,
    PRIMARY KEY (compte_id, noeud_id)
);
CREATE INDEX rangements_noeud ON rangements (noeud_id);

INSERT INTO rangements (compte_id, noeud_id, parent_id, nom, rang)
SELECT p.compte_id, p.noeud_id, NULL, n.nom,
       coalesce((SELECT max(o.rang) + 1 FROM noeuds o WHERE o.proprietaire_id = p.compte_id AND o.parent_id IS NULL), 0)
       + row_number() OVER (PARTITION BY p.compte_id ORDER BY p.cree_le, p.noeud_id) - 1
FROM partages p JOIN noeuds n ON n.id = p.noeud_id
WHERE n.proprietaire_id <> p.compte_id
ON CONFLICT DO NOTHING;

WITH RECURSIVE bas (compte_id, id, parent_id, nom, rang) AS (
    SELECT p.compte_id, e.id, e.parent_id, e.nom, e.rang
    FROM partages p JOIN noeuds r ON r.id = p.noeud_id JOIN noeuds e ON e.parent_id = r.id
    WHERE r.proprietaire_id <> p.compte_id
    UNION
    SELECT b.compte_id, e.id, e.parent_id, e.nom, e.rang FROM bas b JOIN noeuds e ON e.parent_id = b.id
)
INSERT INTO rangements (compte_id, noeud_id, parent_id, nom, rang)
SELECT compte_id, id, parent_id, nom, rang FROM bas
ON CONFLICT DO NOTHING;
