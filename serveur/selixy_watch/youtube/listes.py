import re

from selixy_watch.configuration import MAX_YT_API, MAX_YT_PLAYLIST
from selixy_watch.erreurs import ErreurImport
from selixy_watch.liens.reseau import json_apres, secondes, telecharger, texte_yt, trouver
from selixy_watch.texte import propre
from selixy_watch.youtube.api import api_youtube, details_api
from selixy_watch.youtube.cle import cle_youtube
from selixy_watch.youtube.recherche import MOTIF_DONNEES


def videos_liste_api(lid):
    ids, jeton = [], None
    while len(ids) < MAX_YT_API:
        p = {"part": "contentDetails", "playlistId": lid, "maxResults": 50}
        if jeton:
            p["pageToken"] = jeton
        d = api_youtube("playlistItems", p, 1)
        ids += [(it.get("contentDetails") or {}).get("videoId") for it in d.get("items", [])]
        jeton = d.get("nextPageToken")
        if not jeton:
            break
    ids = [i for i in ids if i][:MAX_YT_API]
    sortie = []
    for k in range(0, len(ids), 50):
        det = details_api(ids[k:k + 50])
        for i in ids[k:k + 50]:
            x = det.get(i)
            if x and x["integrable"] and not x["direct"] and x["duree"] > 0:
                sortie.append((i, x["nom"], x["duree"]))
    return sortie


def videos_presentation_actuelle(data, sortie):
    for r in trouver(data, "lockupViewModel"):
        try:
            duree = next((secondes(t) for t in trouver(r.get("contentImage"), "text") if isinstance(t, str) and re.fullmatch(r"\d+(:\d\d){1,2}", t)), None)
            titre = r["metadata"]["lockupMetadataViewModel"]["title"]["content"]
            if r.get("contentType") == "LOCKUP_CONTENT_TYPE_VIDEO" and r.get("contentId") and duree and r["contentId"] not in [x[0] for x in sortie]:
                sortie.append((r["contentId"], propre(titre, 120) or "Sans titre", duree))
        except (KeyError, TypeError, AttributeError):
            pass


def videos_liste_pages(lid):
    data = json_apres(telecharger(f"https://www.youtube.com/playlist?list={lid}"), MOTIF_DONNEES)
    if data is None:
        raise ErreurImport("Playlist YouTube introuvable (est-elle publique ?).")
    sortie = []
    for r in trouver(data, "playlistVideoRenderer"):
        try:
            if r.get("videoId") and float(r.get("lengthSeconds", 0)) > 0:
                sortie.append((r["videoId"], propre(texte_yt(r.get("title")), 120) or "Sans titre", float(r["lengthSeconds"])))
        except (ValueError, AttributeError):
            pass
    videos_presentation_actuelle(data, sortie)
    return sortie[:MAX_YT_PLAYLIST]


def videos_liste(lid):
    if cle_youtube():
        try:
            return videos_liste_api(lid)
        except ErreurImport:
            pass
    return videos_liste_pages(lid)
