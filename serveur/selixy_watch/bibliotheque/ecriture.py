from contextlib import contextmanager

from selixy_watch.bdd.connexion import transaction
from selixy_watch.etat import verrou


@contextmanager
def ecriture():
    with verrou, transaction() as cx:
        yield cx
