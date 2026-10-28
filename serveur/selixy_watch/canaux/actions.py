from selixy_watch.bibliotheque.lecture import est_playlist
from selixy_watch.canaux import commandes_base as base
from selixy_watch.canaux import commandes_suite as suite
from selixy_watch.canaux.ordre import etat_vide, normaliser
from selixy_watch.canaux.publication import publier
from selixy_watch.erreurs import Refus
from selixy_watch.etat import CANAUX, verrou
from selixy_watch.persistance import ecrire_json

COMMANDES = {
    "lire": base.lire,
    "pause": base.pause,
    "aller": base.aller,
    "jouer": base.jouer,
    "suivant": base.suivant,
    "precedent": suite.precedent,
    "fin": suite.fin,
    "boucle": suite.boucle,
    "aleatoire": suite.aleatoire,
}


def action_canal(cx, cid, action, d):
    with verrou:
        if not est_playlist(cx, cid):
            raise Refus(404, "playlist inconnue")
        e = CANAUX.setdefault(cid, etat_vide())
        normaliser(cx, cid, e)
        commande = COMMANDES.get(action)
        if commande is None:
            raise Refus(404, "action inconnue")
        nouvelle_version = commande(cx, cid, e, d)
        if nouvelle_version is None:
            return {"ok": 1}
        if nouvelle_version:
            e["v"] += 1
        ecrire_json("canaux.json", CANAUX)
        publier(cx, cid, e)
    return {"ok": 1}
