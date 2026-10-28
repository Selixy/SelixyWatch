from selixy_watch.bdd.connexion import transaction
from selixy_watch.comptes.frein import bloque, echec
from selixy_watch.comptes.inscription import entetes_session
from selixy_watch.comptes.jetons_courriel import consommer, creer
from selixy_watch.comptes.mdp import hacher, valider_mdp
from selixy_watch.comptes.ouverture import ouvrir
from selixy_watch.comptes.profils import forme
from selixy_watch.comptes.pseudo import canonique
from selixy_watch.comptes.requete import adresse_client, agent_client
from selixy_watch.courriel import envoi, gabarits
from selixy_watch.entrees.echange import corps_json
from selixy_watch.erreurs import Refus

DEMANDES_PAR_HEURE = 5
HEURE = 3600
LIEN_PERIME = "Ce lien a expiré ou a déjà servi."


def chercher(cx, identifiant):
    return cx.execute(
        "SELECT id, email FROM comptes WHERE email_valide_le IS NOT NULL AND NOT ephemere AND (pseudo_canonique = %s OR lower(email) = %s)",
        (canonique(identifiant), identifiant.strip().lower()),
    ).fetchone()


def demander(h):
    identifiant = str(corps_json(h).get("identifiant", ""))[:254]
    cles = (("recuperation-ip", adresse_client(h)), ("recuperation-id", canonique(identifiant)))
    if bloque(cles, HEURE, DEMANDES_PAR_HEURE):
        raise Refus(429, "Trop de demandes. Réessayez plus tard.")
    echec(cles, HEURE)
    with transaction() as cx:
        compte = chercher(cx, identifiant)
        jeton = creer(cx, compte["id"], "recuperation", compte["email"]) if compte else None
    if jeton:
        sujet, texte = gabarits.recuperation(jeton)
        envoi.envoyer(compte["email"], sujet, texte)
    return 200, {"ok": 1}


def changer(h):
    corps = corps_json(h)
    mdp = valider_mdp(corps.get("mdp"))
    with transaction() as cx:
        jeton = consommer(cx, corps.get("jeton"), "recuperation")
        ligne = cx.execute(
            "UPDATE comptes SET mdp_hash = %s WHERE id = %s AND lower(email) = lower(%s) AND email_valide_le IS NOT NULL "
            "RETURNING id, pseudo, avatar, avatar_version",
            (hacher(mdp), jeton["compte_id"], jeton["email"]),
        ).fetchone()
        if not ligne:
            raise Refus(410, LIEN_PERIME)
        cx.execute("DELETE FROM sessions WHERE compte_id = %s", (ligne["id"],))
        session = ouvrir(cx, ligne["id"], agent_client(h))
    return 200, forme(ligne), entetes_session(session)
