import secrets

from selixy_watch.bdd.connexion import transaction
from selixy_watch.comptes.frein import bloque, echec, reussite
from selixy_watch.comptes.mdp import EMPREINTE_LEURRE, hacher, valider_mdp, verifier
from selixy_watch.comptes.profils import forme
from selixy_watch.comptes.pseudo import canonique, squelette, valider
from selixy_watch.comptes.pseudo_libre import ecrire_sans_doublon
from selixy_watch.comptes.requete import adresse_client, agent_client
from selixy_watch.comptes.ouverture import ouvrir
from selixy_watch.comptes.session import DUREE_JOURS, cookie
from selixy_watch.entrees.echange import corps_json
from selixy_watch.erreurs import Refus

ECHEC_CONNEXION = "Pseudo ou mot de passe incorrect."
EFFACER_ANCIEN = ("Set-Cookie", "mu=; Path=/; Max-Age=0; HttpOnly; SameSite=Lax")


def entetes_session(jeton):
    return [("Set-Cookie", cookie(jeton, DUREE_JOURS * 24 * 3600)), EFFACER_ANCIEN]


def inscription(h):
    corps = corps_json(h)
    pseudo = valider(str(corps.get("pseudo", "")))
    empreinte = hacher(valider_mdp(corps.get("mdp")))
    identifiant = secrets.token_hex(8)

    def ecrire(cx):
        ligne = cx.execute(
            "INSERT INTO comptes (id, pseudo, pseudo_canonique, pseudo_squelette, mdp_hash) VALUES (%s, %s, %s, %s, %s) "
            "RETURNING id, pseudo, avatar, avatar_version",
            (identifiant, pseudo, canonique(pseudo), squelette(pseudo), empreinte),
        ).fetchone()
        return forme(ligne), ouvrir(cx, identifiant, agent_client(h))

    public, jeton = ecrire_sans_doublon(pseudo, ecrire)
    return 201, public, entetes_session(jeton)


def authentifier(cx, canon, mdp):
    ligne = cx.execute(
        "SELECT id, pseudo, avatar, avatar_version, mdp_hash, ephemere FROM comptes WHERE pseudo_canonique = %s", (canon,)
    ).fetchone()
    if not ligne or ligne["ephemere"]:
        verifier(mdp, EMPREINTE_LEURRE)
        return None, False
    if ligne["mdp_hash"] is None:
        valider_mdp(mdp)
        fixe = cx.execute("UPDATE comptes SET mdp_hash = %s WHERE id = %s AND mdp_hash IS NULL", (hacher(mdp), ligne["id"]))
        return (ligne, True) if fixe.rowcount else (None, False)
    return (ligne, False) if verifier(mdp, ligne["mdp_hash"]) else (None, False)


def connexion(h):
    corps = corps_json(h)
    canon = canonique(str(corps.get("pseudo", "")))[:64]
    cles = (("ip", adresse_client(h)), ("pseudo", canon))
    if bloque(cles):
        raise Refus(429, "Trop d'échecs de connexion. Réessayez dans quelques minutes.")
    with transaction() as cx:
        ligne, active = authentifier(cx, canon, str(corps.get("mdp", "")))
        if ligne:
            jeton = ouvrir(cx, ligne["id"], agent_client(h))
    if not ligne:
        echec(cles)
        raise Refus(401, ECHEC_CONNEXION)
    reussite(("pseudo", canon))
    return 200, {**forme(ligne), **({"active": True} if active else {})}, entetes_session(jeton)
