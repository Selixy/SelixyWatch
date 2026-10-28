from selixy_watch.comptes import session
from selixy_watch.erreurs import Refus


def exiger_connecte(h):
    ident = session.ident(h)
    if not ident:
        raise Refus(401, "Connectez-vous d'abord.")
    return ident
