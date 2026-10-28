NOEUDS_VISIBLES = """
WITH RECURSIVE vus (id, niveau) AS (
    SELECT id, 3 FROM noeuds WHERE proprietaire_id = %(c)s
    UNION ALL
    SELECT n.id, CASE p.role WHEN 'editeur' THEN 2 ELSE 1 END
    FROM partages p JOIN noeuds n ON n.id = p.noeud_id
    WHERE p.compte_id = %(c)s AND n.proprietaire_id <> %(c)s
    UNION ALL
    SELECT n.id, v.niveau FROM noeuds n JOIN vus v ON n.parent_id = v.id WHERE n.proprietaire_id <> %(c)s
)
SELECT n.id, n.parent_id, n.type, n.nom, n.rang, n.proprietaire_id, v.niveau,
       r.noeud_id IS NOT NULL AS a_ligne, r.parent_id AS ligne_parent, r.nom AS ligne_nom, r.rang AS ligne_rang
FROM (SELECT id, max(niveau) AS niveau FROM vus GROUP BY id) v
JOIN noeuds n ON n.id = v.id
LEFT JOIN rangements r ON r.noeud_id = n.id AND r.compte_id = %(c)s
ORDER BY coalesce(r.rang, n.rang), n.cree_le
"""


def vue_du_noeud(ligne, compte, visibles):
    if ligne["a_ligne"]:
        parent, nom, rang = ligne["ligne_parent"], ligne["ligne_nom"] or ligne["nom"], ligne["ligne_rang"]
    else:
        parent, nom, rang = ligne["parent_id"], ligne["nom"], ligne["rang"]
    if parent not in visibles or parent == ligne["id"]:
        parent = None
    recu = ligne["proprietaire_id"] != compte and ligne["parent_id"] not in visibles
    return {"id": ligne["id"], "parent": parent, "type": ligne["type"], "nom": nom, "rang": rang,
            "proprietaire_id": ligne["proprietaire_id"], "niveau": ligne["niveau"], "partage_racine": recu}


def charger(cx, compte):
    lignes = cx.execute(NOEUDS_VISIBLES, {"c": compte}).fetchall()
    visibles = {ligne["id"] for ligne in lignes}
    return {ligne["id"]: vue_du_noeud(ligne, compte, visibles) for ligne in lignes}
