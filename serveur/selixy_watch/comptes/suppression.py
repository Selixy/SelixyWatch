from selixy_watch.bdd.connexion import transaction
from selixy_watch.comptes.exigences import exiger_ident, exiger_mdp
from selixy_watch.comptes.purge import achever, purger_compte
from selixy_watch.comptes.session import cookie
from selixy_watch.diffusion.presence import diffuser_presence
from selixy_watch.entrees.echange import corps_json


def supprimer(h):
    i = exiger_ident(h)
    mdp = corps_json(h).get("mdp")
    with transaction() as cx:
        exiger_mdp(cx, i, mdp)
        purge = purger_compte(cx, i)
    achever([purge])
    diffuser_presence()
    return 200, {"ok": 1}, [("Set-Cookie", cookie("", 0))]
