import time

from selixy_watch.configuration import MAX_UNITES
from selixy_watch.erreurs import ErreurImport
from selixy_watch.etat import UNITES, verrou_unites


def reserver_unites(cout):
    jour = time.strftime("%Y-%m-%d", time.gmtime())
    with verrou_unites:
        if UNITES["jour"] != jour:
            UNITES.update(jour=jour, n=0)
        if UNITES["n"] + cout > MAX_UNITES:
            raise ErreurImport("Le quota YouTube du jour est presque atteint, réessayez demain.")
        UNITES["n"] += cout
