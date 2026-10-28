import os

from selixy_watch.comptes.profils import effacer_avatar
from selixy_watch.configuration import DOSSIER_MEDIAS

TRANSFERER = """
UPDATE medias m SET proprietaire_id = x.nouveau
FROM (
    SELECT DISTINCT ON (pm.media_id) pm.media_id, n.proprietaire_id AS nouveau
    FROM playlist_medias pm
    JOIN noeuds n ON n.id = pm.playlist_id
    JOIN medias mm ON mm.id = pm.media_id
    WHERE mm.proprietaire_id = %(c)s AND n.proprietaire_id <> %(c)s
      AND NOT EXISTS (SELECT 1 FROM medias d WHERE d.proprietaire_id = n.proprietaire_id
                      AND d.reference_youtube IS NOT NULL AND d.reference_youtube = mm.reference_youtube)
    ORDER BY pm.media_id, pm.id
) x
WHERE m.id = x.media_id
"""

CONCERNES = """
SELECT p.compte_id AS compte FROM partages p JOIN noeuds n ON n.id = p.noeud_id WHERE n.proprietaire_id = %(c)s
UNION SELECT n.proprietaire_id FROM partages p JOIN noeuds n ON n.id = p.noeud_id WHERE p.compte_id = %(c)s
"""

CANDIDATS_ORPHELINS = """
SELECT DISTINCT pm.media_id AS id FROM playlist_medias pm JOIN noeuds n ON n.id = pm.playlist_id
JOIN medias m ON m.id = pm.media_id WHERE n.proprietaire_id = %(c)s AND m.proprietaire_id <> %(c)s
"""


def supprimer_fichiers(medias):
    for m in medias:
        for nom in (m["fichier"], f"{m['id']}-mini.jpg"):
            try:
                os.remove(os.path.join(DOSSIER_MEDIAS, nom or "-"))
            except (FileNotFoundError, IsADirectoryError):
                pass


def achever(purges):
    from selixy_watch.diffusion.bibliotheque import signaler

    concernes = set()
    for purge in purges:
        supprimer_fichiers(purge["medias"])
        effacer_avatar(purge["compte"])
        concernes |= purge["concernes"]
    signaler(concernes)


def purger_compte(cx, compte):
    cx.execute(TRANSFERER, {"c": compte})
    concernes = {ligne["compte"] for ligne in cx.execute(CONCERNES, {"c": compte})} - {compte}
    candidats = [ligne["id"] for ligne in cx.execute(CANDIDATS_ORPHELINS, {"c": compte})]
    propres = cx.execute("SELECT id, fichier FROM medias WHERE proprietaire_id = %s", (compte,)).fetchall()
    cx.execute("DELETE FROM playlist_medias WHERE media_id = ANY(%s)", ([m["id"] for m in propres],))
    cx.execute("DELETE FROM comptes WHERE id = %s", (compte,))
    orphelins = cx.execute(
        "DELETE FROM medias WHERE id = ANY(%s) AND NOT EXISTS (SELECT 1 FROM playlist_medias WHERE media_id = medias.id) "
        "RETURNING id, fichier",
        (candidats,),
    ).fetchall()
    return {"compte": compte, "concernes": concernes, "medias": propres + orphelins}
