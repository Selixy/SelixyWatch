from selixy_watch.acces.droits import role_sur
from selixy_watch.canaux.avance import etat_public
from selixy_watch.chat.historique import derniers
from selixy_watch.etat import CANAUX
from selixy_watch.vocal.etats import signal_initial


def canaux_accessibles(cx, compte):
    return {cid: etat_public(cx, e, cid) for cid, e in CANAUX.items() if role_sur(cx, compte, cid)}


def evenements_de_depart(cx, canal, compte):
    depart = [("canaux", canaux_accessibles(cx, compte))]
    if canal:
        depart.append(("chat", {"canal": canal, "messages": derniers(cx, canal)}))
        depart.append(signal_initial(canal))
    return depart
