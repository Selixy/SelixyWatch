import os
import uuid

from selixy_watch.acces import droits
from selixy_watch.arbre.orphelins import supprimer_fichier
from selixy_watch.bibliotheque.connecte import exiger_connecte
from selixy_watch.bibliotheque.ecriture import ecriture
from selixy_watch.configuration import DOSSIER_MEDIAS, MAX_MEDIA
from selixy_watch.diffusion.bibliotheque import signaler
from selixy_watch.entrees.echange import longueur_annoncee
from selixy_watch.erreurs import Refus
from selixy_watch.formats import extension_media
from selixy_watch.medias.description import decrire_media
from selixy_watch.medias.enregistrement import enregistrer, verifier_destination


def ecrire_envoi(h, n, mid):
    os.makedirs(DOSSIER_MEDIAS, exist_ok=True)
    tmp = os.path.join(DOSSIER_MEDIAS, mid + ".part")
    reste, ext, genre = n, None, None
    try:
        with open(tmp, "wb") as f:
            while reste > 0:
                bloc = h.rfile.read(min(1 << 20, reste))
                if not bloc:
                    raise Refus(400, "Envoi interrompu.")
                if ext is None:
                    ext, genre = extension_media(bloc[:16])
                    if ext is None:
                        raise Refus(415, "Format non reconnu (mp4, webm, mkv, mp3, ogg, flac, wav, m4a).")
                f.write(bloc)
                reste -= len(bloc)
        os.chmod(tmp, 0o644)
        os.replace(tmp, os.path.join(DOSSIER_MEDIAS, f"{mid}.{ext}"))
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)
    return ext, genre


def verifier_envoi(ident, n, playlist):
    if n <= 0:
        raise Refus(400, "Fichier vide.")
    if n > MAX_MEDIA:
        raise Refus(413, f"Fichier trop gros ({MAX_MEDIA // 1024 // 1024} Mo maximum).")
    with ecriture() as cx:
        verifier_destination(cx, ident, playlist, n)


def recevoir_media(h):
    ident = exiger_connecte(h)
    n, playlist = longueur_annoncee(h), h.headers.get("X-Playlist", "")
    verifier_envoi(ident, n, playlist)
    mid = uuid.uuid4().hex[:12]
    ext, genre = ecrire_envoi(h, n, mid)
    media = decrire_media(h, n, ext, genre)
    try:
        with ecriture() as cx:
            reponse = enregistrer(cx, ident, playlist, mid, media)
            concernes = droits.concernes(cx, playlist)
    except Exception:
        supprimer_fichier(mid, f"{mid}.{ext}")
        raise
    signaler(concernes)
    return 201, reponse


ROUTES_POST = [(r"/api/medias", recevoir_media)]
