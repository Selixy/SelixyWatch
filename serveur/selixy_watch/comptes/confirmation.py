import psycopg

from selixy_watch.bdd.connexion import transaction
from selixy_watch.comptes.jetons_courriel import consommer
from selixy_watch.entrees.echange import corps_json
from selixy_watch.erreurs import Refus


def valider_adresse(cx, compte, adresse):
    try:
        cx.execute(
            "UPDATE comptes SET email = %s, email_valide_le = now(), email_en_attente = NULL WHERE id = %s", (adresse, compte)
        )
    except psycopg.errors.UniqueViolation:
        raise Refus(409, "Cette adresse est déjà utilisée par un autre compte.")


def confirmer(h):
    jeton = corps_json(h).get("jeton")
    with transaction() as cx:
        ligne = consommer(cx, jeton, "confirmation")
        valider_adresse(cx, ligne["compte_id"], ligne["email"])
    return 200, {"email": ligne["email"]}
