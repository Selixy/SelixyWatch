import time
import urllib.parse

from selixy_watch.erreurs import ErreurImport
from selixy_watch.etat import CACHE_YT
from selixy_watch.liens.reseau import json_apres, secondes, telecharger, texte_yt, trouver
from selixy_watch.texte import propre
from selixy_watch.youtube.api import api_youtube, details_api
from selixy_watch.youtube.cle import cle_youtube

MOTIF_DONNEES = r"ytInitialData[\"\]]*\s*=\s*"
VALIDITE_CACHE = 3600


def recherche_api(q, n):
    d = api_youtube("search", {"part": "id", "type": "video", "videoEmbeddable": "true", "maxResults": min(n * 2, 25), "q": q}, 100)
    ids = [(it.get("id") or {}).get("videoId") for it in d.get("items", [])]
    ids = [i for i in ids if i]
    if not ids:
        return []
    det, sortie = details_api(ids), []
    for i in ids:
        x = det.get(i)
        if x and x["integrable"] and not x["direct"] and x["duree"] > 0:
            sortie.append({"yt": i, "nom": x["nom"], "auteur": x["auteur"], "duree": x["duree"]})
    return sortie[:n]


def recherche_pages(q, n=12):
    data = json_apres(telecharger("https://www.youtube.com/results?search_query=" + urllib.parse.quote(q)), MOTIF_DONNEES)
    if data is None:
        raise ErreurImport("La recherche YouTube n'a pas répondu, réessayez dans un instant.")
    sortie, maintenant = [], time.time()
    for r in trouver(data, "videoRenderer"):
        if not isinstance(r, dict) or not r.get("videoId"):
            continue
        d = secondes(texte_yt(r.get("lengthText")))
        if not d:
            continue
        nom = propre(texte_yt(r.get("title")), 120) or "Sans titre"
        auteur = propre(texte_yt(r.get("ownerText")) or texte_yt(r.get("longBylineText")), 60)
        sortie.append({"yt": r["videoId"], "nom": nom, "auteur": auteur, "duree": d})
        CACHE_YT[r["videoId"]] = (nom, float(d), maintenant)
        if len(sortie) == n:
            break
    for k in [k for k, v in CACHE_YT.items() if maintenant - v[2] > VALIDITE_CACHE]:
        del CACHE_YT[k]
    return sortie


def rechercher_youtube(q, n=12):
    erreur, sortie = None, []
    try:
        sortie = recherche_pages(q, n)
    except ErreurImport as e:
        erreur = e
    if not sortie and cle_youtube():
        try:
            sortie = recherche_api(q, n)
            maintenant = time.time()
            for x in sortie:
                CACHE_YT[x["yt"]] = (x["nom"], float(x["duree"]), maintenant)
            erreur = None
        except ErreurImport as e:
            erreur = erreur or e
    if erreur and not sortie:
        raise erreur
    return sortie
