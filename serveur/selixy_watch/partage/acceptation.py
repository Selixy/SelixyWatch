from selixy_watch.acces.droits import role_sur
from selixy_watch.erreurs import Refus
from selixy_watch.partage import invitation_noeuds, invitations, partages
from selixy_watch.partage.copie import copier_arbre
from selixy_watch.partage.offre_pro import accorder_pro, pro_a_donner
from selixy_watch.partage.jetons import hacher


def a_accorder(cx, compte, noeuds):
    return [n for n in noeuds if role_sur(cx, compte, n["id"]) not in ("editeur", "proprietaire")]


def accepter(cx, compte, jeton):
    hache = hacher(jeton)
    invitation = invitations.par_jeton(cx, hache)
    noeuds = invitation_noeuds.de_invitation(cx, invitation["id"]) if invitation else []
    if not noeuds:
        raise Refus(404, "Invitation inconnue.")
    manquants = a_accorder(cx, compte, noeuds)
    pro = pro_a_donner(cx, compte, invitation)
    if not manquants and not (pro and invitation["valide"]):
        return {"noeuds": noeuds, "deja": True, "pro": False}
    if not invitations.consommer(cx, hache):
        raise Refus(410, "Cette invitation a expiré ou n'a plus d'usage.")
    for noeud in manquants:
        partages.accorder(cx, noeud["id"], compte, "editeur")
    if manquants:
        copier_arbre(cx, compte, [noeud["id"] for noeud in manquants])
    return {"noeuds": noeuds, "deja": False, "pro": pro and accorder_pro(cx, compte)}
