from selixy_watch.bibliotheque.lecture import pistes
from selixy_watch.canaux.avance import demarrer
from selixy_watch.canaux.ordre import normaliser, ordre_actif
from selixy_watch.canaux.publication import publier
from selixy_watch.etat import CANAUX, ETATS_VOCAL, verrou
from selixy_watch.persistance import ecrire_json


def avant_retrait(cx, pid, mid):
    with verrou:
        e = CANAUX.get(pid)
        if not e or e["courant"] != mid:
            return
        liste = ordre_actif(cx, pid, e)
        i = liste.index(mid) if mid in liste else 0
        prochain = next((x for x in liste[i + 1:] + liste[:i] if x != mid), None)
        if prochain:
            demarrer(e, prochain)
        else:
            e.update(courant=None, lecture=False, pos=0.0)
        e["v"] += 1


def playlist_modifiee(cx, pid):
    with verrou:
        e = CANAUX.get(pid)
        if e is None:
            return
        normaliser(cx, pid, e)
        if e["courant"] and e["courant"] not in pistes(cx, pid):
            e.update(courant=None, lecture=False, pos=0.0)
            e["v"] += 1
        ecrire_json("canaux.json", CANAUX)
        publier(cx, pid, e)


def playlist_supprimee(pid):
    with verrou:
        CANAUX.pop(pid, None)
        for cle in [k for k in ETATS_VOCAL if k[0] == pid]:
            del ETATS_VOCAL[cle]
        ecrire_json("canaux.json", CANAUX)
