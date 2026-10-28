import json
import re

from selixy_watch.configuration import MAX_LIEN
from selixy_watch.erreurs import ErreurImport
from selixy_watch.liens.reseau import telecharger, trouver
from selixy_watch.texte import propre
from selixy_watch.youtube.recherche import rechercher_youtube

TOLERANCE_DUREE = 10
ILLISIBLE = "Lien Spotify illisible (est-il public ?)."


def pistes_spotify(type_, sid):
    page = telecharger(f"https://open.spotify.com/embed/{type_}/{sid}")
    m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', page, re.S)
    try:
        data = json.loads(m.group(1))
    except (AttributeError, ValueError):
        raise ErreurImport(ILLISIBLE)
    entite = next((e for e in trouver(data, "entity") if isinstance(e, dict) and (e.get("trackList") or e.get("artists") or e.get("name"))), None)
    if not entite:
        raise ErreurImport(ILLISIBLE)
    sortie = []
    for t in entite.get("trackList") or [entite]:
        artistes = ", ".join(a.get("name", "") for a in t.get("artists") or [] if isinstance(a, dict)) or t.get("subtitle") or ""
        artistes = re.sub(r",(?=\S)", ", ", artistes)
        titre, ms = t.get("title") or t.get("name"), t.get("duration")
        if titre and isinstance(ms, (int, float)) and ms > 0:
            sortie.append((propre(artistes, 80), propre(titre, 80), ms / 1000))
    if not sortie:
        raise ErreurImport("Aucun morceau lisible dans ce lien Spotify.")
    return sortie[:MAX_LIEN]


def chercher_youtube(artistes, titre, duree):
    candidats = [(x["yt"], x["duree"]) for x in rechercher_youtube(f"{artistes} {titre}", 5)]
    if not candidats:
        return None
    proche = min(candidats, key=lambda c: abs(c[1] - duree))
    return (proche if abs(proche[1] - duree) < TOLERANCE_DUREE else candidats[0])[0]


def trouver_piste(p):
    try:
        return chercher_youtube(p[0], p[1], p[2])
    except ErreurImport:
        return None
