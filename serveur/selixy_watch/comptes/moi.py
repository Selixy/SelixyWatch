from selixy_watch.bdd.connexion import transaction
from selixy_watch.comptes.exigences import est_ephemere, exiger_ident, exiger_mdp
from selixy_watch.comptes.mdp import hacher, valider_mdp
from selixy_watch.comptes.offre import SELECTION_MOI, champs_courriel
from selixy_watch.comptes.profils import forme
from selixy_watch.comptes.pseudo import canonique, squelette, valider
from selixy_watch.comptes.pseudo_libre import ecrire_sans_doublon
from selixy_watch.comptes.session import DUREE_JOURS, cookie, hacher_jeton, ident, jeton_de
from selixy_watch.diffusion.presence import diffuser_presence
from selixy_watch.entrees.echange import corps_json
from selixy_watch.erreurs import Refus


def moi(h, url):
    i = ident(h)
    if not i:
        return 200, {"anonyme": True}
    with transaction() as cx:
        ligne = cx.execute(SELECTION_MOI, (i,)).fetchone()
    corps = {**forme(ligne), "utilise": int(ligne["utilise"]), "quota": None if ligne["admin"] else ligne["quota_octets"], "ephemere": ligne["ephemere"], **champs_courriel(ligne)}
    entetes = [("Set-Cookie", cookie(jeton_de(h), DUREE_JOURS * 24 * 3600))] if h.ident_session[1] else []
    return 200, corps, entetes


def renommer(h):
    i = exiger_ident(h)
    pseudo = valider(str(corps_json(h).get("pseudo", "")))

    def ecrire(cx):
        ligne = cx.execute(
            "UPDATE comptes SET pseudo = %s, pseudo_canonique = %s, pseudo_squelette = %s WHERE id = %s "
            "RETURNING id, pseudo, avatar, avatar_version",
            (pseudo, canonique(pseudo), squelette(pseudo), i),
        ).fetchone()
        return forme(ligne)

    public = ecrire_sans_doublon(pseudo, ecrire, sauf=i)
    diffuser_presence()
    return 200, public


def changer_mdp(h):
    i = exiger_ident(h)
    corps = corps_json(h)
    nouveau = valider_mdp(corps.get("nouveau"))
    with transaction() as cx:
        if est_ephemere(cx, i):
            raise Refus(403, "Un compte invité n'a pas de mot de passe.")
        exiger_mdp(cx, i, corps.get("ancien"))
        cx.execute("UPDATE comptes SET mdp_hash = %s WHERE id = %s", (hacher(nouveau), i))
        cx.execute("DELETE FROM sessions WHERE compte_id = %s AND jeton_hash <> %s", (i, hacher_jeton(jeton_de(h))))
    return 200, {"ok": 1}
