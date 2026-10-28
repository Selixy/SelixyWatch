import os

from selixy_watch.bdd.connexion import transaction
from selixy_watch.comptes.exigences import exiger_ident
from selixy_watch.comptes.profils import effacer_avatar, forme
from selixy_watch.configuration import DOSSIER_AVATARS, MAX_AVATAR
from selixy_watch.diffusion.presence import diffuser_presence
from selixy_watch.entrees.echange import longueur_annoncee
from selixy_watch.erreurs import Refus
from selixy_watch.formats import extension_image
from selixy_watch.persistance import ecrire_fichier_public


def changer_avatar_en_base(i, ext):
    with transaction() as cx:
        return forme(cx.execute(
            "UPDATE comptes SET avatar = %s, avatar_version = avatar_version + 1 WHERE id = %s "
            "RETURNING id, pseudo, avatar, avatar_version",
            (ext, i),
        ).fetchone())


def avatar(h):
    i = exiger_ident(h)
    n = longueur_annoncee(h)
    if not 0 < n <= MAX_AVATAR:
        raise Refus(413, "Image trop lourde (64 Ko maximum).")
    data = h.rfile.read(n)
    ext = extension_image(data[:16])
    if not ext:
        raise Refus(415, "Image png, jpeg ou webp attendue.")
    effacer_avatar(i)
    ecrire_fichier_public(os.path.join(DOSSIER_AVATARS, f"{i}.{ext}"), data)
    public = changer_avatar_en_base(i, ext)
    diffuser_presence()
    return 200, public


def supprimer_avatar(h):
    i = exiger_ident(h)
    effacer_avatar(i)
    changer_avatar_en_base(i, None)
    diffuser_presence()
    return 200, {"ok": 1}
