from selixy_watch.acces.droits import exiger
from selixy_watch.bibliotheque.lecture import est_playlist
from selixy_watch.comptes.session import ident
from selixy_watch.erreurs import Refus


def compte_autorise(cx, h, cid):
    compte = ident(h)
    if not compte:
        raise Refus(401, "Connectez-vous d'abord.")
    if not est_playlist(cx, cid):
        raise Refus(404, "room inconnue")
    exiger(cx, compte, cid, "lecteur")
    return compte
