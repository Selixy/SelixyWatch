from selixy_watch.erreurs import Refus

ECRIRE_LIGNE = """
INSERT INTO rangements (compte_id, noeud_id, parent_id, rang) VALUES (%s, %s, %s, %s)
ON CONFLICT (compte_id, noeud_id) DO UPDATE SET parent_id = EXCLUDED.parent_id, rang = EXCLUDED.rang
"""

NOMMER_LIGNE = """
INSERT INTO rangements (compte_id, noeud_id, parent_id, nom, rang) VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (compte_id, noeud_id) DO UPDATE SET nom = EXCLUDED.nom
"""


def chez_soi(vue, compte, parent):
    return parent is None or vue[parent]["proprietaire_id"] == compte


def ecrire(cx, compte, vue, n, parent, rang):
    if n["proprietaire_id"] == compte and chez_soi(vue, compte, parent):
        cx.execute("UPDATE noeuds SET parent_id = %s, rang = %s WHERE id = %s", (parent, rang, n["id"]))
        cx.execute("DELETE FROM rangements WHERE compte_id = %s AND noeud_id = %s", (compte, n["id"]))
    else:
        cx.execute(ECRIRE_LIGNE, (compte, n["id"], parent, rang))


def nommer(cx, compte, n, nom):
    if n["proprietaire_id"] == compte:
        cx.execute("UPDATE noeuds SET nom = %s WHERE id = %s", (nom, n["id"]))
        cx.execute("UPDATE rangements SET nom = NULL WHERE compte_id = %s AND noeud_id = %s", (compte, n["id"]))
    else:
        cx.execute(NOMMER_LIGNE, (compte, n["id"], n["parent"], nom, n["rang"]))


def ordre_apres(vue, nid, parent, avant):
    freres = [n["id"] for n in vue.values() if n["parent"] == parent and n["id"] != nid]
    if avant is None:
        return freres + [nid]
    if avant == nid or avant not in freres:
        raise Refus(400, "position invalide")
    freres.insert(freres.index(avant), nid)
    return freres
