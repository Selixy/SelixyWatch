import os

from selixy_watch.bibliotheque.connecte import exiger_connecte
from selixy_watch.bibliotheque.ecriture import ecriture
from selixy_watch.bibliotheque.visibilite import concernes_media
from selixy_watch.configuration import DOSSIER_MEDIAS, MAX_MINIATURE
from selixy_watch.diffusion.bibliotheque import signaler
from selixy_watch.entrees.echange import longueur_annoncee
from selixy_watch.erreurs import Refus
from selixy_watch.persistance import ecrire_fichier_public


def miniature(h, mid):
    ident = exiger_connecte(h)
    n = longueur_annoncee(h)
    if not 0 < n <= MAX_MINIATURE:
        raise Refus(413, "Miniature trop lourde (200 Ko maximum).")
    data = h.rfile.read(n)
    if data[:3] != b"\xff\xd8\xff":
        raise Refus(415, "Image jpeg attendue.")
    with ecriture() as cx:
        ligne = cx.execute("SELECT 1 FROM medias WHERE id = %s AND proprietaire_id = %s AND source = 'fichier'", (mid, ident)).fetchone()
        if not ligne:
            raise Refus(404, "média inconnu")
        ecrire_fichier_public(os.path.join(DOSSIER_MEDIAS, f"{mid}-mini.jpg"), data)
        cx.execute("UPDATE medias SET miniature = true WHERE id = %s", (mid,))
        concernes = concernes_media(cx, mid)
    signaler(concernes)
    return 200, {"ok": 1}


ROUTES_POST = [(r"/api/medias/([0-9a-f]{12})/miniature", miniature)]
