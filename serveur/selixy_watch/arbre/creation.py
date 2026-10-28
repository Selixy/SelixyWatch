import uuid

from selixy_watch.acces import droits
from selixy_watch.arbre.lecture import noeud, nombre, profondeur
from selixy_watch.arbre.rangs import rang_fin
from selixy_watch.bibliotheque.champs import identifiant
from selixy_watch.configuration import MAX_NOEUDS, MAX_PROFONDEUR, RACINE
from selixy_watch.erreurs import Refus
from selixy_watch.texte import propre


def emplacement(cx, ident, parent):
    if parent == RACINE:
        return ident, None, 0
    droits.exiger(cx, ident, parent, "editeur")
    n = noeud(cx, parent)
    if n["type"] != "dossier":
        raise Refus(400, "nom, type ou dossier invalide")
    return n["proprietaire_id"], parent, profondeur(cx, parent)


def creer(cx, ident, d):
    parent = identifiant(d.get("parent", RACINE), "nom, type ou dossier invalide")
    nom, type_ = propre(d.get("nom", ""), 60), d.get("type", "dossier")
    if not nom or type_ not in ("dossier", "playlist"):
        raise Refus(400, "nom, type ou dossier invalide")
    proprietaire, parent_id, niveau = emplacement(cx, ident, parent)
    if niveau >= MAX_PROFONDEUR or nombre(cx, proprietaire) >= MAX_NOEUDS:
        raise Refus(507, "Trop de dossiers imbriqués ou de playlists.")
    nid = uuid.uuid4().hex[:12]
    cx.execute(
        "INSERT INTO noeuds (id, proprietaire_id, parent_id, type, nom, rang) VALUES (%s, %s, %s, %s, %s, %s)",
        (nid, proprietaire, parent_id, type_, nom, rang_fin(cx, proprietaire, parent_id, None)),
    )
    return {"ok": 1, "id": nid}, droits.concernes(cx, nid) | {proprietaire}
