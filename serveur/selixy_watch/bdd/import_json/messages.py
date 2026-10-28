def convertir(chat, ids_playlists, ids_comptes):
    sortie, ignores = [], 0
    for canal, liste in chat.items():
        if canal not in ids_playlists:
            ignores += len(liste)
            continue
        for m in liste:
            auteur = m.get("auteur") or {}
            ident = auteur.get("id")
            sortie.append({"canal_id": canal, "compte_id": ident if ident in ids_comptes else None,
                           "pseudo": str(auteur.get("pseudo") or "Inconnu"), "texte": str(m.get("texte") or ""), "t": m.get("t") or 0})
    return sortie, ignores
