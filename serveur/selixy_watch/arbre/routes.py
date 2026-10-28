from selixy_watch.arbre.actions import action_arbre
from selixy_watch.bibliotheque.connecte import exiger_connecte
from selixy_watch.entrees.echange import corps_json


def route_arbre(h, action):
    ident = exiger_connecte(h)
    return 200, action_arbre(ident, action, corps_json(h))


ROUTES_POST = [(r"/api/arbre/(creer|renommer|deplacer|supprimer)", route_arbre)]
