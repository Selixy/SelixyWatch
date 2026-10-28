from selixy_watch.bdd.connexion import transaction
from selixy_watch.comptes.profils import publics
from selixy_watch.diffusion.evenements import diffuser
from selixy_watch.etat import ABONNES, verrou


def presence():
    with verrou:
        presents = [(info["canal"], info["ident"]) for info in ABONNES.values() if info["canal"] and info["ident"]]
    with transaction() as cx:
        profils = publics(cx, {ident for _, ident in presents})
    canaux = {}
    for canal, ident in presents:
        if ident in profils:
            canaux.setdefault(canal, {})[ident] = profils[ident]
    return {"canaux": {c: list(m.values()) for c, m in canaux.items()}}


def diffuser_presence():
    donnees = presence()
    with verrou:
        diffuser("presence", donnees)
