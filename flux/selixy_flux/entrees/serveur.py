import logging
import os
from functools import partial
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from selixy_flux.entrees.routes import repondre
from selixy_flux.entrees.services import Services
from selixy_flux.relais.amont import ouvrir
from selixy_flux.relais.service import informations, lire
from selixy_flux.resolution.cache import CacheTemporaire
from selixy_flux.resolution.frein import Frein
from selixy_flux.resolution.medias import identifiant_youtube
from selixy_flux.resolution.ytdlp import resoudre

DUREE_ADRESSE = 1800
DUREE_FREIN = 600


class Requete(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'
    services = None

    def do_GET(self):
        statut, entetes, corps = repondre(self.path.split('?')[0], self.headers.get('Range'), self.services)
        self.send_response(statut)
        for nom, valeur in entetes.items():
            self.send_header(nom, valeur)
        if 'Content-Length' not in entetes:
            self.send_header('Connection', 'close')
            self.close_connection = True
        self.end_headers()
        try:
            for bloc in corps:
                self.wfile.write(bloc)
        except (BrokenPipeError, ConnectionResetError):
            self.close_connection = True

    def log_message(self, *arguments):
        return


def construire_services():
    cache = CacheTemporaire(DUREE_ADRESSE)
    resolution = Frein(DUREE_FREIN).moderer(resoudre)
    medias = os.environ.get('MEDIAS', '/donnees/medias.json')
    return Services(
        partial(identifiant_youtube, medias),
        partial(lire, cache=cache, resoudre=resolution, ouvrir=ouvrir),
        partial(informations, cache=cache, resoudre=resolution),
    )


def demarrer():
    logging.basicConfig(level=logging.INFO, format='%(levelname)s %(name)s %(message)s')
    Requete.services = construire_services()
    port = int(os.environ.get('PORT', '8082'))
    ThreadingHTTPServer((os.environ.get('HOTE', '127.0.0.1'), port), Requete).serve_forever()
