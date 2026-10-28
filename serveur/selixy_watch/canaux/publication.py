from selixy_watch.acces.droits import concernes
from selixy_watch.canaux.avance import etat_public
from selixy_watch.diffusion.evenements import diffuser_acces


def publier(cx, cid, e):
    diffuser_acces(cid, concernes(cx, cid), "canal", {"id": cid, "etat": etat_public(cx, e, cid)})
