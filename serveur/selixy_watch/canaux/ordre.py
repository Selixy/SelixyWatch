import random

from selixy_watch.bibliotheque.lecture import pistes


def etat_vide():
    return {"courant": None, "lecture": False, "pos": 0.0, "t0": 0.0, "v": 0, "boucle": False, "aleatoire": False, "melange": []}


def tirer_melange(cx, cid, e):
    ordre = pistes(cx, cid)
    autres = [m for m in ordre if m != e["courant"]]
    random.shuffle(autres)
    e["melange"] = ([e["courant"]] if e["courant"] in ordre else []) + autres


def normaliser(cx, cid, e):
    ordre = pistes(cx, cid)
    if not e["aleatoire"]:
        e["melange"] = []
        return
    melange = [m for m in dict.fromkeys(e["melange"]) if m in ordre]
    for m in ordre:
        if m not in melange:
            i = melange.index(e["courant"]) + 1 if e["courant"] in melange else 0
            melange.insert(random.randint(i, len(melange)), m)
    e["melange"] = melange


def ordre_actif(cx, cid, e):
    return e["melange"] if e["aleatoire"] else pistes(cx, cid)


def suite(cx, cid, e):
    liste = ordre_actif(cx, cid, e)
    if e["courant"] not in liste:
        return list(liste)
    i = liste.index(e["courant"])
    return liste[i + 1:] + liste[:i]
