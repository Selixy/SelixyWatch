from selixy_watch.bdd.connexion import transaction
from selixy_watch.bibliotheque.connecte import exiger_connecte
from selixy_watch.bibliotheque.vue import vue
from selixy_watch.erreurs import Refus


def route_bibliotheque(h, url):
    try:
        ident = exiger_connecte(h)
    except Refus as r:
        return r.code, {"erreur": r.message}
    with transaction() as cx:
        return 200, vue(cx, ident)


ROUTES_GET = {"/api/bibliotheque": route_bibliotheque}
