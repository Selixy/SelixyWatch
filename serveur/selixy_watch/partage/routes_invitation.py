from selixy_watch.acces.droits import exiger
from selixy_watch.bdd.connexion import transaction
from selixy_watch.comptes import profils, session
from selixy_watch.diffusion import bibliotheque
from selixy_watch.entrees.echange import corps_json
from selixy_watch.erreurs import Refus
from selixy_watch.partage import champs, invitation_noeuds, invitations
from selixy_watch.partage.acceptation import accepter
from selixy_watch.partage.jetons import hacher
from selixy_watch.partage.offre_pro import est_admin


def inviter(h):
    d = corps_json(h)
    noeuds = champs.liste_noeuds(d)
    usages = champs.entier_borne(d, "usages_max", 5, 1, 50)
    jours = champs.entier_borne(d, "jours", 7, 1, 30)
    donne_pro = d.get("pro") is True
    with transaction() as cx:
        moi = session.ident(h)
        for noeud in noeuds:
            exiger(cx, moi, noeud, "proprietaire")
        if donne_pro and not est_admin(cx, moi):
            raise Refus(403, "Seul un administrateur peut offrir le statut Pro.")
        invitation = invitations.creer(cx, noeuds, moi, usages, jours, donne_pro)
        decrits = invitation_noeuds.decrire(cx, noeuds)
    return 201, {**invitation, "lien": f"/invitation/#{invitation['jeton']}", "noeuds": decrits}


def voir(h):
    jeton = champs.chaine(corps_json(h), "jeton")
    with transaction() as cx:
        invitation = invitations.par_jeton(cx, hacher(jeton))
        noeuds = invitation_noeuds.de_invitation(cx, invitation["id"]) if invitation else []
        if not noeuds:
            raise Refus(404, "Invitation inconnue.")
        par = profils.publics(cx, [invitation["cree_par"]]).get(invitation["cree_par"], {})
    return 200, {"noeuds": noeuds, "par": {"pseudo": par.get("pseudo"), "avatar": par.get("avatar")}, "valide": invitation["valide"], "pro": invitation["donne_pro"]}


def accepter_invitation(h):
    jeton = champs.chaine(corps_json(h), "jeton")
    moi = session.ident(h)
    if not moi:
        raise Refus(401, "Connectez-vous d'abord.")
    with transaction() as cx:
        reponse = accepter(cx, moi, jeton)
    if not reponse["deja"]:
        bibliotheque.signaler({moi})
    return 200, reponse
