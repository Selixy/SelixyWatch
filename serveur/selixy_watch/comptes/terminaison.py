from selixy_watch.bdd.connexion import transaction
from selixy_watch.comptes.exigences import est_ephemere
from selixy_watch.comptes.purge import achever, purger_compte
from selixy_watch.diffusion.presence import diffuser_presence


def terminer_si_ephemere(compte):
    if not compte:
        return False
    with transaction() as cx:
        if not est_ephemere(cx, compte):
            return False
        purge = purger_compte(cx, compte)
    achever([purge])
    diffuser_presence()
    return True
