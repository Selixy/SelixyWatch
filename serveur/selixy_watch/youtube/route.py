import urllib.parse

from selixy_watch.erreurs import ErreurImport
from selixy_watch.etat import recherches
from selixy_watch.texte import propre
from selixy_watch.youtube.recherche import rechercher_youtube


def route_recherche(h, url):
    q = propre(urllib.parse.parse_qs(url.query).get("q", [""])[0], 100)
    if len(q) < 2:
        return 200, {"resultats": []}
    if not recherches.acquire(timeout=5):
        return 429, {"erreur": "Trop de recherches en même temps, réessayez dans un instant."}
    try:
        return 200, {"resultats": rechercher_youtube(q)}
    except ErreurImport as e:
        return 502, {"erreur": str(e)}
    finally:
        recherches.release()


ROUTES_GET = {"/api/recherche": route_recherche}
