from selixy_watch.bdd.import_json import medias, messages, noeuds, pseudos
from selixy_watch.comptes.pseudo import canonique


def trouver_proprietaire(profils, valides, finaux, demande):
    cible = canonique(demande)
    for ident, pseudo in finaux.items():
        if ident in valides and (pseudo == demande or canonique(pseudo) == cible):
            return ident
    for ident, p in profils.items():
        if p.get("pseudo") == demande:
            return ident
    return None


def construire(donnees, proprietaire, renommages, dossier):
    profils = donnees["profils"]
    finaux = pseudos.pseudos_finaux(profils, renommages)
    valides, invalides = pseudos.valider_tous(finaux, renommages.get(proprietaire, proprietaire))
    collisions = pseudos.collisions(valides)
    ident = trouver_proprietaire(profils, valides, finaux, proprietaire)
    erreurs = [] if ident else [f"Propriétaire introuvable dans profils.json : {proprietaire!r}"]
    erreurs += [f"Renommage inutile (pseudo inconnu) : {a}" for a in renommages if a not in {p.get("pseudo") for p in profils.values()}]
    liste_noeuds, erreurs_noeuds = noeuds.convertir(donnees["arbre"], ident)
    resume = medias.convertir(donnees["medias"], donnees["arbre"], ident, dossier)
    ids_playlists = {n["id"] for n in liste_noeuds if n["type"] == "playlist"}
    liste_messages, canaux_ignores = messages.convertir(donnees["chat"], ids_playlists, set(valides))
    return {"comptes": pseudos.comptes_a_creer(profils, valides), "noeuds": liste_noeuds, "medias": resume["medias"],
            "pistes": medias.pistes(donnees["arbre"], resume["alias"]), "messages": liste_messages,
            "invalides": invalides, "collisions": collisions, "erreurs": erreurs + erreurs_noeuds,
            "inconnus": resume["inconnus"], "orphelins": resume["orphelins"], "manquants": resume["manquants"],
            "messages_ignores": canaux_ignores, "proprietaire": ident}
