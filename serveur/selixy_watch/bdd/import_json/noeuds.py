def regrouper(arbre, ids_vus, erreurs):
    enfants = {}
    for n in arbre:
        if n.get("id") in ids_vus or n.get("type") not in ("dossier", "playlist"):
            erreurs.append(f"Nœud ignoré ou en double : {n.get('id')!r}")
            continue
        ids_vus.add(n["id"])
        parent = None if n.get("parent") in (None, "racine") else n["parent"]
        enfants.setdefault(parent, []).append(n)
    return enfants


def convertir(arbre, proprietaire_id):
    erreurs, ids_vus = [], set()
    enfants = regrouper(arbre, ids_vus, erreurs)
    sortie, file = [], [None]
    while file:
        parent = file.pop(0)
        for rang, n in enumerate(enfants.get(parent, [])):
            sortie.append({"id": n["id"], "proprietaire_id": proprietaire_id, "parent_id": parent, "type": n["type"],
                           "nom": str(n.get("nom") or "Sans titre"), "rang": rang, "t": n.get("t") or 0})
            file.append(n["id"])
    for parent in set(enfants) - {None} - ids_vus:
        erreurs.append(f"Parent introuvable : {parent!r} ({len(enfants[parent])} nœud(s))")
    return sortie, erreurs
