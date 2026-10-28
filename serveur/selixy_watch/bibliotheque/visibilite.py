from selixy_watch.acces import droits


def media_visible(cx, compte, mid):
    ligne = cx.execute("SELECT proprietaire_id FROM medias WHERE id = %s", (mid,)).fetchone()
    if ligne is None:
        return False
    if ligne["proprietaire_id"] == compte:
        return True
    playlists = cx.execute("SELECT DISTINCT playlist_id FROM playlist_medias WHERE media_id = %s", (mid,))
    return any(droits.role_sur(cx, compte, p["playlist_id"]) for p in playlists)


def concernes_media(cx, mid):
    playlists = cx.execute("SELECT DISTINCT playlist_id FROM playlist_medias WHERE media_id = %s", (mid,)).fetchall()
    concernes = {ligne["proprietaire_id"] for ligne in cx.execute("SELECT proprietaire_id FROM medias WHERE id = %s", (mid,))}
    for p in playlists:
        concernes |= droits.concernes(cx, p["playlist_id"])
    return concernes
