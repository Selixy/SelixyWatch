from selixy_watch.arbre.creation import creer
from selixy_watch.arbre.deplacement import deplacer
from selixy_watch.arbre.renommage import renommer
from selixy_watch.arbre.suppression import supprimer
from selixy_watch.bibliotheque.ecriture import ecriture
from selixy_watch.diffusion.bibliotheque import signaler
from selixy_watch.erreurs import Refus

ACTIONS = {"creer": creer, "renommer": renommer, "deplacer": deplacer, "supprimer": supprimer}


def action_arbre(ident, action, d):
    traitement = ACTIONS.get(action)
    if traitement is None:
        raise Refus(404, "action inconnue")
    with ecriture() as cx:
        reponse, concernes = traitement(cx, ident, d)
    signaler(concernes)
    return reponse
