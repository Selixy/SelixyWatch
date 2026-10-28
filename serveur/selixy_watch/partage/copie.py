from selixy_watch.arbre.lecture import sous_arbre
from selixy_watch.bibliotheque.vue_compte import charger

COPIER = """
INSERT INTO rangements (compte_id, noeud_id, parent_id, nom, rang)
SELECT %(c)s, id, parent_id, nom, rang FROM noeuds WHERE id = ANY(%(ids)s) AND id <> ALL(%(racines)s)
ON CONFLICT DO NOTHING
"""

RACINE_A_LA_SUITE = """
INSERT INTO rangements (compte_id, noeud_id, parent_id, nom, rang)
SELECT %s, id, NULL, nom, %s FROM noeuds WHERE id = %s
ON CONFLICT DO NOTHING
"""


def copier_arbre(cx, compte, racines):
    ids = {n["id"] for racine in racines for n in sous_arbre(cx, racine)}
    vue = charger(cx, compte)
    rangs = [n["rang"] for n in vue.values() if n["parent"] is None and n["id"] not in ids]
    cx.execute(COPIER, {"c": compte, "ids": sorted(ids), "racines": racines})
    for decalage, racine in enumerate(racines):
        cx.execute(RACINE_A_LA_SUITE, (compte, max(rangs, default=-1) + 1 + decalage, racine))
