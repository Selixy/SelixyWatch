QUOTA_PRO = 20 * 1024 ** 3

ACCORDER = """
UPDATE comptes SET offre = 'pro', quota_octets = GREATEST(quota_octets, %s)
WHERE id = %s AND NOT ephemere AND offre <> 'pro'
RETURNING id
"""


def est_admin(cx, compte):
    ligne = cx.execute("SELECT admin FROM comptes WHERE id = %s", (compte,)).fetchone()
    return bool(ligne and ligne["admin"])


def pro_a_donner(cx, compte, invitation):
    if not invitation["donne_pro"]:
        return False
    ligne = cx.execute("SELECT offre, ephemere FROM comptes WHERE id = %s", (compte,)).fetchone()
    return bool(ligne) and not ligne["ephemere"] and ligne["offre"] != "pro"


def accorder_pro(cx, compte):
    return cx.execute(ACCORDER, (QUOTA_PRO, compte)).fetchone() is not None
