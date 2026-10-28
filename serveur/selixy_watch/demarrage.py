import os
import threading
import time
import traceback
from http.server import ThreadingHTTPServer

from selixy_watch.bdd.connexion import transaction
from selixy_watch.bdd.migrations import migrer
from selixy_watch.bibliotheque.export_flux import exporter
from selixy_watch.canaux.rattrapage import horloge
from selixy_watch.comptes.nettoyage import nettoyer
from selixy_watch.configuration import DOSSIER_AVATARS, DOSSIER_MEDIAS, HOTE, PORT
from selixy_watch.entrees.gestionnaire import Gestionnaire

PERIODE_NETTOYAGE = 600


def preparer_base():
    with transaction() as cx:
        migrer(cx)
    exporter()


def entretien():
    while True:
        time.sleep(PERIODE_NETTOYAGE)
        try:
            nettoyer()
        except Exception:
            traceback.print_exc()


def demarrer_serveur():
    for d in (DOSSIER_MEDIAS, DOSSIER_AVATARS):
        os.makedirs(d, exist_ok=True)
    preparer_base()
    nettoyer()
    threading.Thread(target=horloge, daemon=True).start()
    threading.Thread(target=entretien, daemon=True).start()
    serveur = ThreadingHTTPServer((HOTE, PORT), Gestionnaire)
    serveur.daemon_threads = True
    serveur.serve_forever()
