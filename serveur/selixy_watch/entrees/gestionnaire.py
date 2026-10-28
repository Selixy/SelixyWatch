import urllib.parse
from http.server import BaseHTTPRequestHandler

from selixy_watch.entrees.echange import repondre
from selixy_watch.entrees.routes_get import ROUTES_GET
from selixy_watch.entrees.routes_post import ROUTES_POST
from selixy_watch.erreurs import Refus


def traiter(h, appel):
    try:
        reponse = appel()
        if reponse is not None:
            repondre(h, *reponse)
    except Refus as r:
        repondre(h, r.code, {"erreur": r.message})
    except (ValueError, KeyError, TypeError):
        repondre(h, 400, {"erreur": "requête invalide"})


def aiguiller(h, routes, chemin, *debut):
    for motif, traitement in routes:
        correspondance = motif.fullmatch(chemin)
        if correspondance:
            return traitement(h, *debut, *correspondance.groups())
    return 404, {"erreur": "inconnu"}


class Gestionnaire(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urllib.parse.urlsplit(self.path)
        traiter(self, lambda: aiguiller(self, ROUTES_GET, url.path, url))

    def do_POST(self):
        traiter(self, lambda: aiguiller(self, ROUTES_POST, self.path.split("?")[0]))

    def log_message(self, *args):
        pass
