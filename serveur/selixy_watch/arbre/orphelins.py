import os

from selixy_watch.configuration import DOSSIER_MEDIAS

ORPHELINS = """
DELETE FROM medias m
WHERE NOT EXISTS (SELECT 1 FROM playlist_medias pm WHERE pm.media_id = m.id)
RETURNING m.id, m.source, m.fichier
"""


def supprimer_fichier(mid, fichier):
    for nom in (fichier, f"{mid}-mini.jpg"):
        try:
            os.remove(os.path.join(DOSSIER_MEDIAS, nom))
        except FileNotFoundError:
            pass


def nettoyer_orphelins(cx):
    supprimes = cx.execute(ORPHELINS).fetchall()
    for ligne in supprimes:
        if ligne["source"] == "fichier" and ligne["fichier"]:
            supprimer_fichier(ligne["id"], ligne["fichier"])
    return len(supprimes)
