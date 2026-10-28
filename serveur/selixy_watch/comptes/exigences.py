from selixy_watch.comptes.frein import bloque, echec, reussite
from selixy_watch.comptes.mdp import verifier
from selixy_watch.comptes.session import ident
from selixy_watch.erreurs import Refus

NON_CONNECTE = "Connectez-vous d'abord."


def exiger_ident(h):
    i = ident(h)
    if not i:
        raise Refus(401, NON_CONNECTE)
    return i


def est_ephemere(cx, compte):
    ligne = cx.execute("SELECT ephemere FROM comptes WHERE id = %s", (compte,)).fetchone()
    return bool(ligne and ligne["ephemere"])


def exiger_mdp(cx, compte, mdp):
    cle = ("mdp", compte)
    if bloque([cle]):
        raise Refus(429, "Trop d'échecs. Réessayez dans quelques minutes.")
    ligne = cx.execute("SELECT mdp_hash FROM comptes WHERE id = %s", (compte,)).fetchone()
    if not ligne or not ligne["mdp_hash"] or not isinstance(mdp, str) or not verifier(mdp, ligne["mdp_hash"]):
        echec([cle])
        raise Refus(401, "Mot de passe incorrect.")
    reussite(cle)
