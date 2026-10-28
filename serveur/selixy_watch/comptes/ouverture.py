import secrets

from selixy_watch.comptes.session import DUREE_JOURS, hacher_jeton


def ouvrir(cx, compte, agent):
    jeton = secrets.token_urlsafe(32)
    cx.execute("DELETE FROM sessions WHERE compte_id = %s AND expire_le < now()", (compte,))
    cx.execute(
        "INSERT INTO sessions (jeton_hash, compte_id, expire_le, agent) VALUES (%s, %s, now() + make_interval(days => %s), %s)",
        (hacher_jeton(jeton), compte, DUREE_JOURS, agent),
    )
    return jeton
