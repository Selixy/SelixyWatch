import time

import psycopg

from selixy_watch.bdd.connexion import transaction
from selixy_watch.canaux.avance import avancer, duree_courante
from selixy_watch.canaux.publication import publier
from selixy_watch.etat import CANAUX, verrou
from selixy_watch.persistance import ecrire_json

PASSES_MAX = 200
TOLERANCE_FIN = 1


def rattraper(cx):
    maintenant, modifie = time.time(), False
    for cid, e in list(CANAUX.items()):
        avance = False
        for _ in range(PASSES_MAX):
            duree = duree_courante(cx, e)
            if not (e["lecture"] and duree > 0):
                break
            fin = e["t0"] + duree - e["pos"]
            if maintenant < fin + TOLERANCE_FIN:
                break
            avancer(cx, cid, e, True)
            if e["lecture"]:
                e["t0"] = fin
            avance = True
        if avance:
            e["v"] += 1
            publier(cx, cid, e)
            modifie = True
    if modifie:
        ecrire_json("canaux.json", CANAUX)


def horloge():
    while True:
        time.sleep(1)
        try:
            with verrou, transaction() as cx:
                rattraper(cx)
        except psycopg.Error:
            continue
