import threading
import time

FENETRE = 15 * 60
ECHECS_MAX = 5

_echecs = {}
_verrou = threading.Lock()


def recents(cle, maintenant, fenetre):
    gardes = [t for t in _echecs.get(cle, []) if maintenant - t < fenetre]
    _echecs[cle] = gardes
    return gardes


def bloque(cles, fenetre=FENETRE, maxi=ECHECS_MAX):
    maintenant = time.time()
    with _verrou:
        return any(len(recents(cle, maintenant, fenetre)) >= maxi for cle in cles)


def echec(cles, fenetre=FENETRE):
    maintenant = time.time()
    with _verrou:
        for cle in cles:
            _echecs[cle] = recents(cle, maintenant, fenetre) + [maintenant]


def reussite(cle):
    with _verrou:
        _echecs.pop(cle, None)


def reinitialiser():
    with _verrou:
        _echecs.clear()
