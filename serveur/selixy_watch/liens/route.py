import threading

from selixy_watch.acces import droits
from selixy_watch.bibliotheque import lecture
from selixy_watch.bibliotheque.connecte import exiger_connecte
from selixy_watch.bibliotheque.ecriture import ecriture
from selixy_watch.entrees.echange import corps_json
from selixy_watch.erreurs import Refus
from selixy_watch.etat import imports
from selixy_watch.liens.analyse import reconnaitre_lien
from selixy_watch.liens.importation import importer


def exiger_playlist_editable(ident, playlist):
    if not isinstance(playlist, str):
        raise Refus(404, "playlist inconnue")
    with ecriture() as cx:
        droits.exiger(cx, ident, playlist, "editeur")
        if not lecture.est_playlist(cx, playlist):
            raise Refus(404, "playlist inconnue")


def demander_import(h):
    ident = exiger_connecte(h)
    d = corps_json(h, 2048)
    playlist = d.get("playlist")
    exiger_playlist_editable(ident, playlist)
    lien = reconnaitre_lien(d.get("url", ""))
    if not lien:
        raise Refus(400, "Lien non reconnu : YouTube ou Spotify seulement.")
    if not imports.acquire(blocking=False):
        raise Refus(429, "Un import est déjà en cours, réessayez dans un instant.")
    try:
        threading.Thread(target=importer, args=(lien, playlist, ident), daemon=True).start()
    except Exception:
        imports.release()
        raise
    return 202, {"ok": 1}


ROUTES_POST = [(r"/api/liens", demander_import)]
