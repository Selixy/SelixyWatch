from selixy_watch.bdd.connexion import transaction
from selixy_watch.canaux.acces_salle import compte_autorise
from selixy_watch.canaux.actions import action_canal
from selixy_watch.entrees.echange import corps_json
from selixy_watch.etat import verrou


def commande_canal(h, cid, action):
    try:
        d = corps_json(h)
    except ValueError:
        d = {}
    with verrou, transaction() as cx:
        compte_autorise(cx, h, cid)
        return 200, action_canal(cx, cid, action, d)


ROUTES_POST = [
    (r"/api/canal/([0-9a-f]{12})/(lire|pause|aller|jouer|suivant|precedent|fin|boucle|aleatoire)", commande_canal),
]
