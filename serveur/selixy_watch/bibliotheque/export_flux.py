from selixy_watch.bdd.connexion import transaction
from selixy_watch.persistance import ecrire_json

FICHIER = "medias.json"


def references_youtube(cx):
    lignes = cx.execute("SELECT id, reference_youtube FROM medias WHERE source = 'youtube' AND reference_youtube IS NOT NULL")
    return {ligne["id"]: {"source": "youtube", "yt": ligne["reference_youtube"]} for ligne in lignes}


def exporter():
    with transaction() as cx:
        references = references_youtube(cx)
    ecrire_json(FICHIER, references, 0o644)
