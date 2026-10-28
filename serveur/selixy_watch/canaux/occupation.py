import time

from selixy_watch.bibliotheque.lecture import est_playlist
from selixy_watch.canaux import commandes_base as base
from selixy_watch.canaux.avance import avancer, duree_courante
from selixy_watch.canaux.ordre import etat_vide, normaliser, ordre_actif
from selixy_watch.canaux.publication import publier
from selixy_watch.erreurs import Refus
from selixy_watch.etat import ABONNES, CANAUX
from selixy_watch.persistance import ecrire_json


def canal_occupe(canal):
    return any(info.get("canal") == canal for info in ABONNES.values())


def auto_demarrer(cx, canal):
    if not canal or not est_playlist(cx, canal):
        return
    e = CANAUX.setdefault(canal, etat_vide())
    normaliser(cx, canal, e)
    duree = duree_courante(cx, e)
    if duree > 0 and e["pos"] >= duree:
        avancer(cx, canal, e, False)
    if not e["lecture"]:
        liste = ordre_actif(cx, canal, e)
        if e["courant"] is not None or liste:
            try:
                base.lire(cx, canal, e, {})
                e["v"] += 1
                ecrire_json("canaux.json", CANAUX)
                publier(cx, canal, e)
            except Refus:
                pass


def auto_mettre_en_pause(cx, canal):
    if not canal or canal_occupe(canal):
        return
    e = CANAUX.get(canal)
    if e and e.get("lecture"):
        e.update(pos=e["pos"] + time.time() - e["t0"], lecture=False)
        e["v"] += 1
        ecrire_json("canaux.json", CANAUX)
        publier(cx, canal, e)
