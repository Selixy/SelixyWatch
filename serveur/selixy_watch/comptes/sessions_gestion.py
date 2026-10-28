from selixy_watch.bdd.connexion import transaction
from selixy_watch.comptes.exigences import exiger_ident
from selixy_watch.comptes.session import cookie, hacher_jeton, ident, jeton_de
from selixy_watch.comptes.terminaison import terminer_si_ephemere
from selixy_watch.entrees.echange import corps_json


def courante(h):
    jeton = jeton_de(h)
    return hacher_jeton(jeton) if jeton else ""


def lister(h, url):
    i = ident(h)
    if not i:
        return 401, {"erreur": "Connectez-vous d'abord."}
    with transaction() as cx:
        lignes = cx.execute(
            "SELECT jeton_hash, agent, EXTRACT(EPOCH FROM cree_le)::bigint AS cree, EXTRACT(EPOCH FROM expire_le)::bigint AS expire "
            "FROM sessions WHERE compte_id = %s AND expire_le > now() ORDER BY cree_le DESC",
            (i,),
        ).fetchall()
    actuelle = courante(h)
    return 200, {"sessions": [
        {"id": s["jeton_hash"][:12], "cree_le": s["cree"], "expire_le": s["expire"], "agent": s["agent"], "courante": s["jeton_hash"] == actuelle}
        for s in lignes
    ]}


def revoquer(h):
    i = exiger_ident(h)
    cible = str(corps_json(h).get("id", ""))
    with transaction() as cx:
        cx.execute("DELETE FROM sessions WHERE compte_id = %s AND left(jeton_hash, 12) = %s", (i, cible))
    return 200, {"ok": 1}


def deconnexion(h):
    if not terminer_si_ephemere(ident(h)):
        with transaction() as cx:
            cx.execute("DELETE FROM sessions WHERE jeton_hash = %s", (courante(h),))
    return 200, {"ok": 1}, [("Set-Cookie", cookie("", 0))]


def deconnexion_partout(h):
    i = exiger_ident(h)
    if not terminer_si_ephemere(i):
        with transaction() as cx:
            cx.execute("DELETE FROM sessions WHERE compte_id = %s", (i,))
    return 200, {"ok": 1}, [("Set-Cookie", cookie("", 0))]
