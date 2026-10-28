from selixy_watch.erreurs import Refus

NIVEAUX = {"lecteur": 1, "editeur": 2, "proprietaire": 3}

CHAINE = """
WITH RECURSIVE chaine AS (
    SELECT id, parent_id, proprietaire_id FROM noeuds WHERE id = %(noeud)s
    UNION ALL
    SELECT n.id, n.parent_id, n.proprietaire_id FROM noeuds n JOIN chaine c ON n.id = c.parent_id
)
"""

ROLE = CHAINE + """
SELECT bool_or(c.proprietaire_id = %(compte)s) AS proprietaire,
       max(CASE p.role WHEN 'editeur' THEN 2 WHEN 'lecteur' THEN 1 END) AS partage
FROM chaine c LEFT JOIN partages p ON p.noeud_id = c.id AND p.compte_id = %(compte)s
"""

CONCERNES = CHAINE + """
SELECT proprietaire_id AS compte FROM chaine
UNION SELECT p.compte_id FROM chaine c JOIN partages p ON p.noeud_id = c.id
"""


def role_sur(connexion, compte, noeud):
    if not compte or not noeud:
        return None
    ligne = connexion.execute(ROLE, {"noeud": noeud, "compte": compte}).fetchone()
    if not ligne or ligne["proprietaire"] is None:
        return None
    if ligne["proprietaire"]:
        return "proprietaire"
    return {2: "editeur", 1: "lecteur"}.get(ligne["partage"])


def exiger(connexion, compte, noeud, minimum):
    if not compte:
        raise Refus(401, "Connectez-vous d'abord.")
    role = role_sur(connexion, compte, noeud)
    if role is None:
        raise Refus(404, "élément inconnu")
    if NIVEAUX[role] < NIVEAUX[minimum]:
        raise Refus(403, "Vous n'avez pas le droit de modifier cet élément.")
    return role


def concernes(connexion, noeud):
    return {ligne["compte"] for ligne in connexion.execute(CONCERNES, {"noeud": noeud})}
