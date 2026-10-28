from selixy_watch.arbre.lecture import sous_arbre

LISTER ="SELECT compte_id FROM partages WHERE noeud_id = %s ORDER BY cree_le"

ACCORDER = """
INSERT INTO partages (noeud_id, compte_id, role) VALUES (%s, %s, %s)
ON CONFLICT (noeud_id, compte_id) DO UPDATE SET role = EXCLUDED.role WHERE EXCLUDED.role = 'editeur'
"""


def lister(cx, noeud):
    return cx.execute(LISTER, (noeud,)).fetchall()


def accorder(cx, noeud, compte, role):
    cx.execute(ACCORDER, (noeud, compte, role))


def retirer(cx, noeud, compte):
    requete = "DELETE FROM partages WHERE noeud_id = %s AND compte_id = %s"
    retire = cx.execute(requete, (noeud, compte)).rowcount > 0
    ids = [ligne["id"] for ligne in sous_arbre(cx, noeud)]
    cx.execute("DELETE FROM rangements WHERE compte_id = %s AND noeud_id = ANY(%s)", (compte, ids))
    return retire
