from selixy_watch.acces import droits
from selixy_watch.bibliotheque import lecture
from selixy_watch.canaux import synchro
from selixy_watch.erreurs import Refus
from selixy_watch.medias.autorisation import exiger_envoi
from selixy_watch.medias.quota import exiger_place


def verifier_destination(cx, ident, playlist, octets):
    droits.exiger(cx, ident, playlist, "editeur")
    if not lecture.est_playlist(cx, playlist):
        raise Refus(404, "playlist inconnue (en-tête X-Playlist)")
    exiger_envoi(cx, ident)
    exiger_place(cx, ident, octets)


def enregistrer(cx, ident, playlist, mid, media):
    verifier_destination(cx, ident, playlist, media["taille"])
    cx.execute(
        "INSERT INTO medias (id, proprietaire_id, source, nom, genre, duree, fichier, taille) VALUES (%s, %s, 'fichier', %s, %s, %s, %s, %s)",
        (mid, ident, media["nom"], media["genre"], media["duree"], f"{mid}.{media['ext']}", media["taille"]),
    )
    cx.execute(
        "INSERT INTO playlist_medias (playlist_id, media_id, rang) "
        "SELECT %s, %s, COALESCE(max(rang) + 1, 0) FROM playlist_medias WHERE playlist_id = %s",
        (playlist, mid, playlist),
    )
    synchro.playlist_modifiee(cx, playlist)
    return {"id": mid, **lecture.media(cx, mid)}
