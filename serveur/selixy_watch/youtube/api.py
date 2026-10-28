import json
import re
import urllib.error
import urllib.parse
import urllib.request

from selixy_watch.erreurs import ErreurImport
from selixy_watch.texte import propre
from selixy_watch.youtube.cle import cle_youtube
from selixy_watch.youtube.quota import reserver_unites


def api_youtube(chemin, params, cout):
    cle = cle_youtube()
    if not cle:
        raise ErreurImport("Pas de clé d'API YouTube.")
    reserver_unites(cout)
    url = f"https://www.googleapis.com/youtube/v3/{chemin}?" + urllib.parse.urlencode({**params, "key": cle})
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"Accept": "application/json"}), timeout=15) as rep:
            return json.loads(rep.read(4 << 20))
    except urllib.error.HTTPError:
        raise ErreurImport("L'API YouTube a refusé la requête (clé ou quota).")
    except (urllib.error.URLError, OSError, ValueError):
        raise ErreurImport("Impossible de joindre l'API YouTube.")


def duree_iso(t):
    m = re.fullmatch(r"P(?:(\d+)D)?(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?)?", t or "")
    if not m:
        return 0.0
    j, h, mi, sec = (int(x or 0) for x in m.groups())
    return float(((j * 24 + h) * 60 + mi) * 60 + sec)


def details_api(ids):
    d = api_youtube("videos", {"part": "snippet,contentDetails,status", "id": ",".join(ids), "maxResults": 50}, 1)
    sortie = {}
    for it in d.get("items", []):
        sn, cd, st = it.get("snippet") or {}, it.get("contentDetails") or {}, it.get("status") or {}
        sortie[it.get("id")] = {
            "nom": propre(sn.get("title", ""), 120) or "Sans titre", "auteur": propre(sn.get("channelTitle", ""), 60),
            "duree": duree_iso(cd.get("duration")), "integrable": bool(st.get("embeddable", True)),
            "direct": sn.get("liveBroadcastContent", "none") != "none",
        }
    return sortie
