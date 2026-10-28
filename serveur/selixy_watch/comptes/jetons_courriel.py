import secrets

from selixy_watch.comptes.session import hacher_jeton
from selixy_watch.erreurs import Refus

DUREES = {"confirmation": "24 hours", "recuperation": "1 hour"}


def creer(cx, compte, nature, email):
    cx.execute("DELETE FROM jetons_courriel WHERE compte_id = %s AND nature = %s AND utilise_le IS NULL", (compte, nature))
    jeton = secrets.token_urlsafe(32)
    cx.execute(
        "INSERT INTO jetons_courriel (jeton_hash, compte_id, nature, email, expire_le) VALUES (%s, %s, %s, %s, now() + %s::interval)",
        (hacher_jeton(jeton), compte, nature, email, DUREES[nature]),
    )
    return jeton


def consommer(cx, jeton, nature):
    empreinte = hacher_jeton(jeton) if isinstance(jeton, str) else ""
    ligne = cx.execute(
        "UPDATE jetons_courriel SET utilise_le = now() WHERE jeton_hash = %s AND nature = %s AND utilise_le IS NULL AND expire_le > now() "
        "RETURNING compte_id, email",
        (empreinte, nature),
    ).fetchone()
    if not ligne:
        raise Refus(410, "Ce lien a expiré ou a déjà servi.")
    return ligne
