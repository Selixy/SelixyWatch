import re
import time

from selixy_watch.bibliotheque.routes import ROUTES_GET as ROUTES_BIBLIOTHEQUE
from selixy_watch.comptes.routes import ROUTES_GET as ROUTES_COMPTES
from selixy_watch.flux.sse import ROUTES_GET as ROUTES_FLUX
from selixy_watch.partage.routes import ROUTES_GET as ROUTES_PARTAGE
from selixy_watch.youtube.cle import cle_youtube
from selixy_watch.youtube.route import ROUTES_GET as ROUTES_RECHERCHE


def sante(h, url):
    return 200, {"ok": 1, "cle_youtube": bool(cle_youtube())}


def heure(h, url):
    return 200, {"t": time.time()}


TABLE = {"/api/sante": sante, "/api/heure": heure, **ROUTES_COMPTES, **ROUTES_RECHERCHE, **ROUTES_FLUX, **ROUTES_PARTAGE, **ROUTES_BIBLIOTHEQUE}

ROUTES_GET = [(re.compile(re.escape(chemin)), traitement) for chemin, traitement in TABLE.items()]
