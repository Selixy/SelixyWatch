def est_playlist(connexion, nid):
    return connexion.execute("SELECT 1 FROM noeuds WHERE id = %s AND type = 'playlist'", (nid,)).fetchone() is not None


def pistes(connexion, pid):
    lignes = connexion.execute("SELECT media_id FROM playlist_medias WHERE playlist_id = %s ORDER BY rang, id", (pid,))
    return [ligne["media_id"] for ligne in lignes]


def forme_publique(ligne):
    media = {"nom": ligne["nom"], "genre": ligne["genre"], "duree": float(ligne["duree"]), "t": int(ligne["cree_le"].timestamp())}
    if ligne["source"] == "youtube":
        return {**media, "source": "youtube", "yt": ligne["reference_youtube"]}
    return {**media, "ext": ligne["fichier"].rsplit(".", 1)[-1], "taille": ligne["taille"], "mini": ligne["miniature"]}


def media(connexion, mid):
    ligne = connexion.execute("SELECT * FROM medias WHERE id = %s", (mid,)).fetchone()
    return forme_publique(ligne) if ligne else None
