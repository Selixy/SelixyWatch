import queue

from selixy_watch.etat import ABONNES


def envoyer(q, evenement, donnees):
    try:
        q.put_nowait((evenement, donnees))
    except queue.Full:
        ABONNES.pop(q, None)


def diffuser(evenement, donnees):
    for q in list(ABONNES):
        envoyer(q, evenement, donnees)


def diffuser_canal(canal, evenement, donnees):
    for q, info in list(ABONNES.items()):
        if info["canal"] == canal:
            envoyer(q, evenement, donnees)


def diffuser_acces(canal, comptes, evenement, donnees):
    for q, info in list(ABONNES.items()):
        if info["canal"] == canal or info["ident"] in comptes:
            envoyer(q, evenement, donnees)
