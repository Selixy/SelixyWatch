import time

from selixy_watch.bdd.connexion import transaction
from selixy_watch.canaux.acces_salle import compte_autorise
from selixy_watch.chat.historique import enregistrer
from selixy_watch.comptes.profils import public
from selixy_watch.configuration import EMOJIS, MAX_TEXTE
from selixy_watch.diffusion.evenements import diffuser_canal
from selixy_watch.entrees.echange import corps_json
from selixy_watch.erreurs import Refus
from selixy_watch.etat import DERNIER_MESSAGE, DERNIERE_REACTION, verrou
from selixy_watch.texte import propre


def message(h, cid):
    texte = propre(corps_json(h).get("texte", ""), MAX_TEXTE)
    if not texte:
        raise Refus(400, "Message vide.")
    with verrou, transaction() as cx:
        i = compte_autorise(cx, h, cid)
        maintenant = time.time()
        if maintenant - DERNIER_MESSAGE.get(i, 0) < 0.7:
            raise Refus(429, "Doucement : un message à la fois.")
        DERNIER_MESSAGE[i] = maintenant
        msg = enregistrer(cx, cid, public(i), texte)
        diffuser_canal(cid, "chat", {"canal": cid, "message": msg})
    return 200, {"ok": 1}


def reaction(h, cid):
    emoji = corps_json(h).get("emoji")
    if emoji not in EMOJIS:
        raise Refus(400, "Réaction inconnue.")
    with verrou, transaction() as cx:
        i = compte_autorise(cx, h, cid)
        maintenant = time.time()
        if maintenant - DERNIERE_REACTION.get(i, 0) < 0.3:
            raise Refus(429, "Doucement.")
        DERNIERE_REACTION[i] = maintenant
        diffuser_canal(cid, "reaction", {"canal": cid, "auteur": public(i), "emoji": emoji})
    return 200, {"ok": 1}


ROUTES_POST = [
    (r"/api/canal/([0-9a-f]{12})/message", message),
    (r"/api/canal/([0-9a-f]{12})/reaction", reaction),
]
