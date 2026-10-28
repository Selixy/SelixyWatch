from psycopg.errors import UniqueViolation

from selixy_watch.bdd.connexion import transaction
from selixy_watch.comptes.pseudo import canonique, squelette
from selixy_watch.erreurs import Refus

DEJA_PRIS = "Ce pseudo est déjà pris."
RESSEMBLE = "Ce pseudo ressemble trop à un compte existant."


def exiger_libre(cx, pseudo, sauf=None):
    ligne = cx.execute(
        "SELECT id, pseudo_canonique FROM comptes WHERE (pseudo_canonique = %s OR pseudo_squelette = %s) AND id IS DISTINCT FROM %s",
        (canonique(pseudo), squelette(pseudo), sauf),
    ).fetchone()
    if ligne:
        raise Refus(409, DEJA_PRIS if ligne["pseudo_canonique"] == canonique(pseudo) else RESSEMBLE)


def ecrire_sans_doublon(pseudo, ecriture, sauf=None):
    try:
        with transaction() as cx:
            exiger_libre(cx, pseudo, sauf)
            return ecriture(cx)
    except UniqueViolation:
        with transaction() as cx:
            exiger_libre(cx, pseudo, sauf)
        raise Refus(409, DEJA_PRIS)
