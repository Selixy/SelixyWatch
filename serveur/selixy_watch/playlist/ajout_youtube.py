import uuid

from selixy_watch.acces import droits
from selixy_watch.bibliotheque import lecture
from selixy_watch.bibliotheque.ecriture import ecriture

NIVEAUX_EDITION = ("editeur", "proprietaire")


def media_youtube(cx, compte, yt, nom, duree):
    ligne = cx.execute("SELECT id FROM medias WHERE proprietaire_id = %s AND reference_youtube = %s", (compte, yt)).fetchone()
    if ligne:
        return ligne["id"]
    mid = uuid.uuid4().hex[:12]
    cx.execute(
        "INSERT INTO medias (id, proprietaire_id, source, reference_youtube, nom, genre, duree) VALUES (%s, %s, 'youtube', %s, %s, 'video', %s)",
        (mid, compte, yt, nom, round(duree, 2)),
    )
    return mid


def ajouter_youtube(playlist, compte, yt, nom, duree):
    with ecriture() as cx:
        if not lecture.est_playlist(cx, playlist) or droits.role_sur(cx, compte, playlist) not in NIVEAUX_EDITION:
            return False
        mid = media_youtube(cx, compte, yt, nom, duree)
        if mid in lecture.pistes(cx, playlist):
            return False
        cx.execute(
            "INSERT INTO playlist_medias (playlist_id, media_id, rang) "
            "SELECT %s, %s, COALESCE(max(rang) + 1, 0) FROM playlist_medias WHERE playlist_id = %s",
            (playlist, mid, playlist),
        )
        return True
