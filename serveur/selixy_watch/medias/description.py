import re
import urllib.parse

from selixy_watch.texte import propre

SUFFIXES = r"\.(mp4|m4v|mov|webm|mkv|mp3|ogg|oga|opus|flac|wav|m4a|aac)$"


def decrire_media(h, n, ext, genre):
    try:
        duree = float(h.headers.get("X-Duree", "0"))
    except ValueError:
        duree = 0.0
    nom = re.sub(SUFFIXES, "", propre(urllib.parse.unquote(h.headers.get("X-Nom", "")), 130), flags=re.I)
    return {"nom": nom[:120] or "Sans titre", "ext": ext, "genre": genre, "taille": n,
            "duree": round(max(0.0, min(duree, 86400.0)), 2) if duree == duree else 0.0}
