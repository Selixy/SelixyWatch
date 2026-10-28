import time

from selixy_watch.bibliotheque.lecture import pistes
from selixy_watch.canaux.avance import avancer, demarrer
from selixy_watch.canaux.ordre import ordre_actif
from selixy_watch.erreurs import Refus


def lire(cx, cid, e, d):
    liste = ordre_actif(cx, cid, e)
    if e["courant"] is None:
        if not liste:
            raise Refus(400, "Cette playlist ne contient aucun média.")
        demarrer(e, liste[0])
    elif not e["lecture"]:
        e.update(lecture=True, t0=time.time())
    return True


def pause(cx, cid, e, d):
    if e["lecture"]:
        e.update(pos=e["pos"] + time.time() - e["t0"], lecture=False)
    return True


def aller(cx, cid, e, d):
    pos = d.get("pos")
    if isinstance(pos, bool) or not isinstance(pos, (int, float)) or pos != pos or e["courant"] is None:
        raise Refus(400, "position invalide")
    e.update(pos=max(0.0, float(pos)), t0=time.time())
    return True


def jouer(cx, cid, e, d):
    if d.get("media") not in pistes(cx, cid):
        raise Refus(404, "média absent de cette playlist")
    demarrer(e, d["media"])
    return True


def suivant(cx, cid, e, d):
    avancer(cx, cid, e, False)
    return True
