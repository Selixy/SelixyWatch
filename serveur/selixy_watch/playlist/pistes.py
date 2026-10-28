from selixy_watch.arbre.orphelins import nettoyer_orphelins
from selixy_watch.bibliotheque.visibilite import media_visible
from selixy_watch.canaux import synchro
from selixy_watch.erreurs import Refus


def rang_de(cx, pid, mid):
    ligne = cx.execute("SELECT rang FROM playlist_medias WHERE playlist_id = %s AND media_id = %s", (pid, mid)).fetchone()
    return None if ligne is None else ligne["rang"]


def place(cx, pid, mid, avant):
    if avant is None:
        ligne = cx.execute(
            "SELECT max(rang) AS m FROM playlist_medias WHERE playlist_id = %s AND media_id <> %s", (pid, mid)
        ).fetchone()
        return 0 if ligne["m"] is None else ligne["m"] + 1
    rang = rang_de(cx, pid, avant)
    if rang is None or avant == mid:
        raise Refus(400, "position invalide")
    cx.execute("UPDATE playlist_medias SET rang = rang + 1 WHERE playlist_id = %s AND rang >= %s AND media_id <> %s", (pid, rang, mid))
    return rang


def ajouter(cx, ident, pid, mid, avant):
    if not media_visible(cx, ident, mid):
        raise Refus(404, "média inconnu")
    if rang_de(cx, pid, mid) is not None:
        raise Refus(409, "Ce média est déjà dans la playlist.")
    cx.execute(
        "INSERT INTO playlist_medias (playlist_id, media_id, rang) VALUES (%s, %s, %s)", (pid, mid, place(cx, pid, mid, avant))
    )


def retirer(cx, ident, pid, mid, avant):
    if rang_de(cx, pid, mid) is None:
        raise Refus(404, "média absent de la playlist")
    synchro.avant_retrait(cx, pid, mid)
    cx.execute("DELETE FROM playlist_medias WHERE playlist_id = %s AND media_id = %s", (pid, mid))
    nettoyer_orphelins(cx)


def deplacer(cx, ident, pid, mid, avant):
    if rang_de(cx, pid, mid) is None:
        raise Refus(400, "position invalide")
    rang = place(cx, pid, mid, avant)
    cx.execute("UPDATE playlist_medias SET rang = %s WHERE playlist_id = %s AND media_id = %s", (rang, pid, mid))
