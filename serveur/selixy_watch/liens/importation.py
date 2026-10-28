import concurrent.futures

from selixy_watch.diffusion.evenements import diffuser
from selixy_watch.erreurs import ErreurImport
from selixy_watch.etat import imports, verrou
from selixy_watch.liens.suivi import SuiviImport
from selixy_watch.spotify.pistes import pistes_spotify, trouver_piste
from selixy_watch.texte import propre
from selixy_watch.youtube.listes import videos_liste
from selixy_watch.youtube.video import info_video

PARALLELISME_SPOTIFY = 4


def importer_video(cible, suivi):
    titre, duree = info_video(cible)
    suivi.ajouter(cible, titre, duree)


def importer_liste(cible, suivi):
    videos = videos_liste(cible)
    if not videos:
        raise ErreurImport("Aucune vidéo lisible dans cette playlist YouTube.")
    for vid, titre, duree in videos:
        suivi.ajouter(vid, titre, duree)


def importer_spotify(cible, suivi):
    pistes = pistes_spotify(*cible)
    manques = 0
    with concurrent.futures.ThreadPoolExecutor(PARALLELISME_SPOTIFY) as pool:
        for p, vid in zip(pistes, pool.map(trouver_piste, pistes)):
            if vid:
                suivi.ajouter(vid, propre(f"{p[0]} – {p[1]}" if p[0] else p[1], 120), p[2])
            else:
                manques += 1
    if manques:
        return f"{manques} morceau{'x' if manques > 1 else ''} introuvable{'s' if manques > 1 else ''} sur YouTube."
    return None


SOURCES = {"video": importer_video, "liste": importer_liste, "spotify": importer_spotify}


def importer(lien, playlist, compte):
    erreur, suivi = None, SuiviImport(playlist, compte)
    with verrou:
        diffuser("import", {"playlist": playlist, "en_cours": True, "erreur": None})
    try:
        genre, cible = lien
        erreur = SOURCES[genre](cible, suivi)
        if not suivi.ajoutes and not erreur:
            erreur = "Rien de nouveau : tout est déjà dans la playlist."
    except ErreurImport as e:
        erreur = str(e)
    except Exception:
        erreur = "L'import a échoué."
    finally:
        imports.release()
        if suivi.en_attente:
            suivi.publier()
        with verrou:
            diffuser("import", {"playlist": playlist, "en_cours": False, "erreur": erreur})
