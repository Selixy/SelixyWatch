import random
import time

from selixy_watch.bibliotheque.lecture import media
from selixy_watch.canaux.ordre import ordre_actif, suite


def etat_public(cx, e, cid):
    return {**{k: v for k, v in e.items() if k != "melange"}, "suite": suite(cx, cid, e), "t": time.time()}


def duree_courante(cx, e):
    m = media(cx, e["courant"]) if e["courant"] else None
    return m["duree"] if m else 0.0


def demarrer(e, mid):
    e.update(courant=mid, pos=0.0, t0=time.time(), lecture=True)


def avancer(cx, cid, e, naturel):
    if naturel and e["boucle"] and e["courant"]:
        demarrer(e, e["courant"])
        return
    liste = ordre_actif(cx, cid, e)
    i = liste.index(e["courant"]) if e["courant"] in liste else -1
    if i + 1 < len(liste):
        demarrer(e, liste[i + 1])
        return
    if not liste:
        e.update(courant=None, lecture=False, pos=0.0)
        return
    if e["aleatoire"]:
        liste = e["melange"] = random.sample(liste, len(liste))
        if len(liste) > 1 and liste[0] == e["courant"]:
            liste.append(liste.pop(0))
    demarrer(e, liste[0])
