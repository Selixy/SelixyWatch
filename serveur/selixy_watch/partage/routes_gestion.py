import urllib.parse

from selixy_watch.acces.droits import concernes, exiger
from selixy_watch.bdd.connexion import transaction
from selixy_watch.comptes import profils, session
from selixy_watch.diffusion import bibliotheque
from selixy_watch.entrees.echange import corps_json
from selixy_watch.erreurs import Refus
from selixy_watch.partage import champs, invitation_noeuds, invitations, partages


def lire(h, url):
    noeud = urllib.parse.parse_qs(url.query).get("noeud", [""])[0]
    try:
        with transaction() as cx:
            exiger(cx, session.ident(h), noeud, "proprietaire")
            lignes = partages.lister(cx, noeud)
            publics = profils.publics(cx, [ligne["compte_id"] for ligne in lignes])
            invites = [{"compte": publics[ligne["compte_id"]]} for ligne in lignes]
            return 200, {"invites": invites, "invitations": invitation_noeuds.lister(cx, noeud)}
    except Refus as r:
        return r.code, {"erreur": r.message}


def retirer(h, noeud):
    cible = champs.chaine(corps_json(h), "compte")
    with transaction() as cx:
        exiger(cx, session.ident(h), noeud, "proprietaire")
        touches = concernes(cx, noeud)
        if not partages.retirer(cx, noeud, cible):
            raise Refus(404, "Cet invité n'existe pas.")
    bibliotheque.signaler(touches)
    return 200, {"ok": 1}


def revoquer(h, noeud):
    ident = champs.chaine(corps_json(h), "invitation")
    with transaction() as cx:
        exiger(cx, session.ident(h), noeud, "proprietaire")
        if not invitations.revoquer(cx, noeud, ident):
            raise Refus(404, "Invitation inconnue.")
    return 200, {"ok": 1}


def quitter(h, noeud):
    moi = session.ident(h)
    with transaction() as cx:
        exiger(cx, moi, noeud, "lecteur")
        touches = concernes(cx, noeud)
        if not partages.retirer(cx, noeud, moi):
            raise Refus(400, "Seule la racine d'un partage reçu se quitte.")
    bibliotheque.signaler(touches)
    return 200, {"ok": 1}
