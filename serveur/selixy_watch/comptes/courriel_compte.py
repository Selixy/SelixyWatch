import re

from selixy_watch.bdd.connexion import transaction
from selixy_watch.comptes.exigences import est_ephemere, exiger_ident, exiger_mdp
from selixy_watch.comptes.frein import bloque, echec
from selixy_watch.comptes.jetons_courriel import creer
from selixy_watch.courriel import envoi, gabarits
from selixy_watch.entrees.echange import corps_json
from selixy_watch.erreurs import Refus

MOTIF = re.compile(r"^[^@\s]+@[^@\s.]+(\.[^@\s.]+)+$")
ENVOIS_PAR_HEURE = 5
HEURE = 3600


def adresse_valide(brut):
    adresse = str(brut or "").strip().lower()
    if len(adresse) > 254 or not MOTIF.match(adresse):
        raise Refus(400, "Adresse e-mail invalide.")
    return adresse


def enregistrer_en_attente(cx, compte, adresse):
    prise = cx.execute(
        "SELECT 1 FROM comptes WHERE lower(email) = %s AND email_valide_le IS NOT NULL AND id <> %s", (adresse, compte)
    ).fetchone()
    if prise:
        raise Refus(409, "Cette adresse est déjà utilisée par un autre compte.")
    deja = cx.execute("SELECT 1 FROM comptes WHERE id = %s AND lower(email) = %s AND email_valide_le IS NOT NULL", (compte, adresse)).fetchone()
    if deja:
        return None
    cx.execute("UPDATE comptes SET email_en_attente = %s WHERE id = %s", (adresse, compte))
    return creer(cx, compte, "confirmation", adresse)


def definir_email(h):
    compte = exiger_ident(h)
    corps = corps_json(h)
    adresse = adresse_valide(corps.get("email"))
    cle = ("email", compte)
    if bloque([cle], HEURE, ENVOIS_PAR_HEURE):
        raise Refus(429, "Trop d'envois. Réessayez plus tard.")
    with transaction() as cx:
        if est_ephemere(cx, compte):
            raise Refus(403, "Un compte invité n'a pas d'adresse e-mail.")
        exiger_mdp(cx, compte, corps.get("mdp"))
        jeton = enregistrer_en_attente(cx, compte, adresse)
    if jeton is None:
        return 200, {"envoye": False}
    echec([cle], HEURE)
    sujet, texte = gabarits.confirmation(jeton)
    return 200, {"envoye": envoi.envoyer(adresse, sujet, texte)}


def supprimer_email(h):
    compte = exiger_ident(h)
    with transaction() as cx:
        exiger_mdp(cx, compte, corps_json(h).get("mdp"))
        cx.execute("UPDATE comptes SET email = NULL, email_valide_le = NULL, email_en_attente = NULL WHERE id = %s", (compte,))
        cx.execute("DELETE FROM jetons_courriel WHERE compte_id = %s", (compte,))
    return 200, {"ok": 1}
