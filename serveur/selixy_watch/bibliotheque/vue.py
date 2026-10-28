from selixy_watch.bibliotheque import vue_compte
from selixy_watch.bibliotheque.lecture import forme_publique
from selixy_watch.comptes import profils

ROLES = {3: "proprietaire", 2: "editeur", 1: "lecteur"}


def lire_pistes(cx, playlists):
    pistes = {pid: [] for pid in playlists}
    lignes = cx.execute(
        "SELECT playlist_id, media_id FROM playlist_medias WHERE playlist_id = ANY(%s) ORDER BY playlist_id, rang, id", (playlists,)
    )
    for ligne in lignes:
        pistes[ligne["playlist_id"]].append(ligne["media_id"])
    return pistes


def lire_medias(cx, pistes):
    ids = sorted({mid for liste in pistes.values() for mid in liste})
    lignes = cx.execute("SELECT * FROM medias WHERE id = ANY(%s)", (ids,))
    return {ligne["id"]: forme_publique(ligne) for ligne in lignes}


def vue(cx, compte):
    vus = list(vue_compte.charger(cx, compte).values())
    pistes = lire_pistes(cx, [n["id"] for n in vus if n["type"] == "playlist"])
    proprietaires = profils.publics(cx, sorted({n["proprietaire_id"] for n in vus}))
    noeuds = []
    for n in vus:
        noeud = {"id": n["id"], "parent": n["parent"] or "racine", "type": n["type"], "nom": n["nom"], "rang": n["rang"],
                 "role": ROLES[n["niveau"]], "proprietaire": proprietaires.get(n["proprietaire_id"]),
                 "partage_racine": n["partage_racine"]}
        if n["type"] == "playlist":
            noeud["pistes"] = pistes[n["id"]]
        noeuds.append(noeud)
    return {"noeuds": noeuds, "medias": lire_medias(cx, pistes)}
