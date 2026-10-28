from selixy_watch.partage.jetons import nouveau

PAR_JETON = """
SELECT id, jeton_hash, cree_par, donne_pro, (expire_le > now() AND usages < usages_max) AS valide
FROM invitations WHERE jeton_hash = %s
"""

CONSOMMER = """
UPDATE invitations SET usages = usages + 1
WHERE jeton_hash = %s AND usages < usages_max AND expire_le > now()
RETURNING usages
"""

CREER = """
INSERT INTO invitations (id, jeton_hash, cree_par, role, expire_le, usages_max, donne_pro)
VALUES (%s, %s, %s, 'editeur', now() + make_interval(days => %s), %s, %s)
RETURNING extract(epoch FROM expire_le)::bigint AS expire_le
"""

REVOQUER = """
DELETE FROM invitations WHERE id = %s AND EXISTS
    (SELECT 1 FROM invitation_noeuds WHERE invitation_id = %s AND noeud_id = %s)
"""


def creer(cx, noeuds, par, usages_max, jours, donne_pro=False):
    jeton, hache, ident = nouveau()
    ligne = cx.execute(CREER, (ident, hache, par, jours, usages_max, donne_pro)).fetchone()
    for noeud in noeuds:
        cx.execute("INSERT INTO invitation_noeuds (invitation_id, noeud_id) VALUES (%s, %s)", (ident, noeud))
    return {"id": ident, "jeton": jeton, "expire_le": ligne["expire_le"], "pro": donne_pro}


def par_jeton(cx, hache):
    return cx.execute(PAR_JETON, (hache,)).fetchone()


def consommer(cx, hache):
    return cx.execute(CONSOMMER, (hache,)).fetchone() is not None


def revoquer(cx, noeud, ident):
    return cx.execute(REVOQUER, (ident, ident, noeud)).rowcount > 0
