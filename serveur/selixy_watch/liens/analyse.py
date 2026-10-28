import re
import urllib.parse

RE_SPOTIFY_URI = r"spotify:(track|album|playlist):([A-Za-z0-9]{22})"
RE_SPOTIFY_CHEMIN = r"/(?:intl-[a-z-]+/)?(track|album|playlist)/([A-Za-z0-9]{22})(?:/|$)"


def lien_spotify(u):
    m = re.match(RE_SPOTIFY_CHEMIN, u.path)
    return ("spotify", (m.group(1), m.group(2))) if m else None


def lien_youtube(u, req):
    m = re.fullmatch(r"/(?:shorts|embed|live)/([\w-]{11})/?", u.path)
    if m:
        return "video", m.group(1)
    v = req.get("v", [""])[0]
    if u.path == "/watch" and re.fullmatch(r"[\w-]{11}", v):
        return "video", v
    liste = req.get("list", [""])[0]
    if u.path in ("/playlist", "/watch") and re.fullmatch(r"[\w-]{10,64}", liste):
        return "liste", liste
    return None


def reconnaitre_lien(url):
    url = str(url).strip()
    m = re.fullmatch(RE_SPOTIFY_URI, url)
    if m:
        return "spotify", (m.group(1), m.group(2))
    try:
        u = urllib.parse.urlsplit(url if "//" in url else "https://" + url)
        hote = (u.hostname or "").lower()
    except ValueError:
        return None
    if u.scheme not in ("http", "https"):
        return None
    hote = re.sub(r"^(www|m|music)\.", "", hote)
    if hote == "open.spotify.com":
        return lien_spotify(u)
    if hote == "youtu.be":
        m = re.fullmatch(r"/([\w-]{11})/?", u.path)
        return ("video", m.group(1)) if m else None
    if hote == "youtube.com":
        return lien_youtube(u, urllib.parse.parse_qs(u.query))
    return None
