import os

from selixy_watch.bdd.connexion import transaction
from selixy_watch.configuration import DOSSIER_AVATARS


def forme(ligne):
    avatar = f"/avatars/{ligne['id']}.{ligne['avatar']}?v={ligne['avatar_version']}" if ligne["avatar"] else None
    return {"id": ligne["id"], "pseudo": ligne["pseudo"], "avatar": avatar}


def publics(cx, ids):
    ids = list(ids)
    if not ids:
        return {}
    lignes = cx.execute("SELECT id, pseudo, avatar, avatar_version FROM comptes WHERE id = ANY(%s)", (ids,)).fetchall()
    return {ligne["id"]: forme(ligne) for ligne in lignes}


def public(ident):
    with transaction() as cx:
        return publics(cx, [ident]).get(ident)


def effacer_avatar(ident):
    for ext in ("png", "jpg", "webp"):
        try:
            os.remove(os.path.join(DOSSIER_AVATARS, f"{ident}.{ext}"))
        except FileNotFoundError:
            pass
