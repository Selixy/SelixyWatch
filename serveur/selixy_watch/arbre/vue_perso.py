from selixy_watch.configuration import MAX_PROFONDEUR
from selixy_watch.erreurs import Refus


def enfants(vue, parent):
    return [n for n in vue.values() if n["parent"] == parent]


def profondeur(vue, nid):
    niveau = 0
    while nid is not None and niveau <= MAX_PROFONDEUR + 1:
        niveau += 1
        nid = vue[nid]["parent"]
    return niveau


def sous_arbre(vue, nid):
    trouves, pile = [], [nid]
    while pile:
        courant = pile.pop()
        trouves.append(courant)
        pile.extend(n["id"] for n in enfants(vue, courant))
    return trouves


def hauteur(vue, nid):
    dossiers = [n["id"] for n in enfants(vue, nid) if n["type"] == "dossier"]
    return 1 + max(hauteur(vue, d) for d in dossiers) if dossiers else 0


def verifier(vue, nid, vers):
    if vers in sous_arbre(vue, nid):
        raise Refus(400, "Un dossier ne peut pas entrer dans lui-même.")
    propre = hauteur(vue, nid) if vue[nid]["type"] == "dossier" else 0
    if (profondeur(vue, vers) if vers else 0) + 1 + propre > MAX_PROFONDEUR:
        raise Refus(400, "Trop de dossiers imbriqués.")
