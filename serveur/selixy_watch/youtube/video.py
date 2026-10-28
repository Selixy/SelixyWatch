import time

from selixy_watch.erreurs import ErreurImport
from selixy_watch.etat import CACHE_YT
from selixy_watch.liens.reseau import json_apres, telecharger
from selixy_watch.texte import propre
from selixy_watch.youtube.api import details_api
from selixy_watch.youtube.cle import cle_youtube
from selixy_watch.youtube.recherche import VALIDITE_CACHE, rechercher_youtube

INTERDIT_HORS_YOUTUBE = "L'auteur de cette vidéo interdit sa lecture hors de YouTube."
DIRECTS_REFUSES = "Les directs YouTube ne sont pas pris en charge."


def info_par_api(vid):
    try:
        x = details_api([vid]).get(vid)
    except ErreurImport:
        return False
    if x is None:
        raise ErreurImport("Cette vidéo YouTube n'est pas disponible.")
    if x:
        if not x["integrable"]:
            raise ErreurImport(INTERDIT_HORS_YOUTUBE)
        if x["direct"] or x["duree"] <= 0:
            raise ErreurImport(DIRECTS_REFUSES)
        return x["nom"], x["duree"]
    return False


def info_par_page(vid):
    try:
        page = telecharger(f"https://www.youtube.com/watch?v={vid}")
    except ErreurImport:
        page = None
    r = json_apres(page, r"ytInitialPlayerResponse\s*=\s*") if page else None
    d, etat = ((r.get("videoDetails") or {}, r.get("playabilityStatus") or {}) if isinstance(r, dict) else ({}, {}))
    if etat.get("status") == "OK" and d:
        if etat.get("playableInEmbed") is False:
            raise ErreurImport(INTERDIT_HORS_YOUTUBE)
        try:
            duree = float(d.get("lengthSeconds", 0))
        except ValueError:
            duree = 0.0
        if d.get("isLive") or duree <= 0:
            raise ErreurImport(DIRECTS_REFUSES)
        return (propre(d.get("title", ""), 120) or "Sans titre", duree), etat
    return None, etat


def info_video(vid):
    c = CACHE_YT.get(vid)
    if c and time.time() - c[2] < VALIDITE_CACHE:
        return c[0], c[1]
    if cle_youtube():
        trouve = info_par_api(vid)
        if trouve:
            return trouve
    trouve, etat = info_par_page(vid)
    if trouve:
        return trouve
    for x in rechercher_youtube(vid, 8):
        if x["yt"] == vid:
            return x["nom"], float(x["duree"])
    raise ErreurImport("Cette vidéo YouTube n'est pas disponible." if etat else "Vidéo YouTube introuvable.")
