from selixy_watch.acces import droits
from selixy_watch.arbre.lecture import noeud, sous_arbre
from selixy_watch.arbre.orphelins import nettoyer_orphelins
from selixy_watch.bibliotheque.champs import identifiant
from selixy_watch.canaux import synchro
from selixy_watch.erreurs import Refus


def refuser_racine_de_partage(cx, ident, nid):
    n = noeud(cx, nid)
    if n["proprietaire_id"] == ident:
        return
    recu = cx.execute("SELECT 1 FROM partages WHERE noeud_id = %s AND compte_id = %s", (nid, ident)).fetchone()
    if recu:
        raise Refus(403, "Ce dossier vous est partagé : quittez le partage au lieu de le supprimer.")


def supprimer(cx, ident, d):
    nid = identifiant(d.get("id"), "élément inconnu")
    droits.exiger(cx, ident, nid, "editeur")
    refuser_racine_de_partage(cx, ident, nid)
    concernes = droits.concernes(cx, nid)
    playlists = [ligne["id"] for ligne in sous_arbre(cx, nid) if ligne["type"] == "playlist"]
    cx.execute("DELETE FROM noeuds WHERE id = %s", (nid,))
    nettoyer_orphelins(cx)
    for pid in playlists:
        synchro.playlist_supprimee(pid)
    return {"ok": 1}, concernes
