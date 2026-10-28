DE_INVITATION = """
SELECT n.id, n.type, n.nom FROM invitation_noeuds i JOIN noeuds n ON n.id = i.noeud_id
WHERE i.invitation_id = %s ORDER BY n.type, n.nom, n.id
"""

DES_NOEUDS = "SELECT id, type, nom FROM noeuds WHERE id = ANY(%s)"

CONTENANT = """
SELECT v.id, extract(epoch FROM v.expire_le)::bigint AS expire_le, v.usages, v.usages_max
FROM invitations v WHERE EXISTS (SELECT 1 FROM invitation_noeuds WHERE invitation_id = v.id AND noeud_id = %s)
ORDER BY v.cree_le
"""


def de_invitation(cx, invitation):
    return cx.execute(DE_INVITATION, (invitation,)).fetchall()


def decrire(cx, noeuds):
    trouves = {ligne["id"]: ligne for ligne in cx.execute(DES_NOEUDS, (list(noeuds),))}
    return [trouves[n] for n in noeuds if n in trouves]


def lister(cx, noeud):
    invitations = cx.execute(CONTENANT, (noeud,)).fetchall()
    for invitation in invitations:
        invitation["noeuds"] = [{"id": n["id"], "nom": n["nom"]} for n in de_invitation(cx, invitation["id"])]
    return invitations
