import hashlib
import http.cookies

from selixy_watch.bdd.connexion import transaction
from selixy_watch.configuration import COOKIE_SECURE

DUREE_JOURS = 30
PROLONGATION_JOURS = 15
NOM_COOKIE = "session"


def hacher_jeton(jeton):
    return hashlib.sha256(jeton.encode()).hexdigest()


def jeton_de(h):
    c = http.cookies.SimpleCookie(h.headers.get("Cookie", ""))
    return c[NOM_COOKIE].value if NOM_COOKIE in c else None


def cookie(jeton, age):
    return f"{NOM_COOKIE}={jeton}; Path=/; Max-Age={age}; HttpOnly; SameSite=Lax" + ("; Secure" if COOKIE_SECURE else "")


def chercher(jeton):
    empreinte = hacher_jeton(jeton)
    with transaction() as cx:
        prolongee = cx.execute(
            "UPDATE sessions SET expire_le = now() + make_interval(days => %s) WHERE jeton_hash = %s AND expire_le > now() "
            "AND expire_le < now() + make_interval(days => %s) RETURNING compte_id",
            (DUREE_JOURS, empreinte, PROLONGATION_JOURS),
        ).fetchone()
        if prolongee:
            return prolongee["compte_id"], True
        ligne = cx.execute("SELECT compte_id FROM sessions WHERE jeton_hash = %s AND expire_le > now()", (empreinte,)).fetchone()
    return (ligne["compte_id"] if ligne else None), False


def ident(h):
    if not hasattr(h, "ident_session"):
        jeton = jeton_de(h)
        h.ident_session = chercher(jeton) if jeton else (None, False)
    return h.ident_session[0]
