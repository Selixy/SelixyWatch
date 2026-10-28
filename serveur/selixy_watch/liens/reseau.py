import json
import re
import urllib.error
import urllib.request

from selixy_watch.configuration import ENTETES_WEB
from selixy_watch.erreurs import ErreurImport


def telecharger(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=ENTETES_WEB), timeout=15) as r:
            return r.read(8 << 20).decode("utf-8", "replace")
    except (urllib.error.URLError, OSError, ValueError):
        raise ErreurImport("Impossible de joindre le site du lien, réessayez dans un instant.")


def json_apres(page, motif):
    m = re.search(motif, page)
    i = page.find("{", m.end()) if m else -1
    if i < 0:
        return None
    try:
        return json.JSONDecoder().raw_decode(page, i)[0]
    except ValueError:
        return None


def trouver(obj, cle):
    pile = [obj]
    while pile:
        o = pile.pop()
        if isinstance(o, dict):
            if cle in o:
                yield o[cle]
            pile.extend(reversed(list(o.values())))
        elif isinstance(o, list):
            pile.extend(reversed(o))


def texte_yt(t):
    if isinstance(t, dict):
        return t.get("simpleText") or "".join(r.get("text", "") for r in t.get("runs", []) if isinstance(r, dict))
    return ""


def secondes(texte):
    try:
        v = [int(x) for x in str(texte).split(":")]
    except ValueError:
        return None
    return float(sum(x * 60 ** i for i, x in enumerate(reversed(v)))) if v and len(v) <= 3 else None
