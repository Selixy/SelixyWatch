CHAINE = """
WITH RECURSIVE chaine AS (
    SELECT id, parent_id FROM noeuds WHERE id = %s
    UNION ALL
    SELECT n.id, n.parent_id FROM noeuds n JOIN chaine c ON n.id = c.parent_id
)
"""

HAUTEUR = """
WITH RECURSIVE bas AS (
    SELECT id, 0 AS niveau FROM noeuds WHERE id = %s
    UNION ALL
    SELECT n.id, b.niveau + 1 FROM noeuds n JOIN bas b ON n.parent_id = b.id WHERE n.type = 'dossier'
)
SELECT max(niveau) AS hauteur FROM bas
"""

SOUS_ARBRE = """
WITH RECURSIVE bas AS (
    SELECT id, type FROM noeuds WHERE id = %s
    UNION ALL
    SELECT n.id, n.type FROM noeuds n JOIN bas b ON n.parent_id = b.id
)
SELECT id, type FROM bas
"""


def noeud(cx, nid):
    return cx.execute("SELECT * FROM noeuds WHERE id = %s", (nid,)).fetchone()


def profondeur(cx, nid):
    return cx.execute(CHAINE + "SELECT count(*) AS n FROM chaine", (nid,)).fetchone()["n"]


def hauteur(cx, nid):
    return cx.execute(HAUTEUR, (nid,)).fetchone()["hauteur"] or 0


def sous_arbre(cx, nid):
    return cx.execute(SOUS_ARBRE, (nid,)).fetchall()


def nombre(cx, proprietaire):
    return cx.execute("SELECT count(*) AS n FROM noeuds WHERE proprietaire_id = %s", (proprietaire,)).fetchone()["n"]
