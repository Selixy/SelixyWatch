FRATRIE = "proprietaire_id = %(p)s AND parent_id IS NOT DISTINCT FROM %(parent)s AND id IS DISTINCT FROM %(exclu)s"


def rang_fin(cx, proprietaire, parent, exclu):
    parametres = {"p": proprietaire, "parent": parent, "exclu": exclu}
    ligne = cx.execute("SELECT max(rang) AS m FROM noeuds WHERE " + FRATRIE, parametres).fetchone()
    return 0 if ligne["m"] is None else ligne["m"] + 1
