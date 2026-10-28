import os


def references(arbre):
    vus = []
    for n in arbre:
        if n.get("type") == "playlist":
            vus.extend(n.get("pistes") or [])
    return list(dict.fromkeys(vus))


def convertir_un(mid, m, proprietaire_id):
    youtube = m.get("source") == "youtube"
    ext = str(m.get("ext") or "").lstrip(".")
    return {"id": mid, "proprietaire_id": proprietaire_id, "source": "youtube" if youtube else "fichier",
            "reference_youtube": m.get("yt") if youtube else None, "nom": str(m.get("nom") or "Sans titre"),
            "genre": "audio" if m.get("genre") == "audio" else "video", "duree": float(m.get("duree") or 0),
            "fichier": None if youtube else f"{mid}.{ext}", "taille": 0 if youtube else int(m.get("taille") or 0),
            "miniature": bool(m.get("mini")), "t": m.get("t") or 0}


def convertir(medias, arbre, proprietaire_id, dossier):
    utilises = references(arbre)
    sortie, alias, inconnus, premiers = [], {}, [], {}
    for mid in utilises:
        if mid not in medias:
            inconnus.append(mid)
            continue
        ligne = convertir_un(mid, medias[mid], proprietaire_id)
        cle = ligne["reference_youtube"]
        if cle and cle in premiers:
            alias[mid] = premiers[cle]
            continue
        if cle:
            premiers[cle] = mid
        alias[mid] = mid
        sortie.append(ligne)
    orphelins = sorted(set(medias) - set(utilises))
    manquants = [m["fichier"] for m in sortie if m["fichier"] and not os.path.exists(os.path.join(dossier, "medias", m["fichier"]))]
    return {"medias": sortie, "alias": alias, "inconnus": inconnus, "orphelins": orphelins, "manquants": manquants}


def pistes(arbre, alias):
    sortie = []
    for n in arbre:
        if n.get("type") == "playlist":
            ids = [alias[m] for m in n.get("pistes") or [] if m in alias]
            sortie.extend((n["id"], mid, rang) for rang, mid in enumerate(ids))
    return sortie
