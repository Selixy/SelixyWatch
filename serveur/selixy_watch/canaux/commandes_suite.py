import time

from selixy_watch.canaux.avance import avancer, demarrer
from selixy_watch.canaux.ordre import ordre_actif, tirer_melange
from selixy_watch.erreurs import Refus


def precedent(cx, cid, e, d):
    if e["courant"] is not None:
        liste = ordre_actif(cx, cid, e)
        i = liste.index(e["courant"]) if e["courant"] in liste else -1
        ici = e["pos"] + (time.time() - e["t0"] if e["lecture"] else 0.0)
        if ici > 3 or len(liste) < 2:
            e.update(pos=0.0, t0=time.time())
        else:
            demarrer(e, liste[i - 1])
    return True


def fin(cx, cid, e, d):
    if d.get("media") != e["courant"] or d.get("v") != e["v"]:
        return None
    avancer(cx, cid, e, True)
    return True


def actif_demande(d):
    actif = d.get("actif")
    if not isinstance(actif, bool):
        raise Refus(400, "« actif » doit être vrai ou faux")
    return actif


def boucle(cx, cid, e, d):
    e["boucle"] = actif_demande(d)
    return False


def aleatoire(cx, cid, e, d):
    e["aleatoire"] = actif_demande(d)
    if e["aleatoire"]:
        tirer_melange(cx, cid, e)
    else:
        e["melange"] = []
    return False
