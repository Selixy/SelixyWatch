import json
import re

from selixy_flux.journal import journal

MOTIF_YOUTUBE = re.compile(r'[A-Za-z0-9_-]{11}')


def identifiant_youtube(chemin, media):
    try:
        with open(chemin, encoding='utf-8') as fichier:
            medias = json.load(fichier)
    except (OSError, ValueError) as erreur:
        journal.error('lecture de %s impossible : %s', chemin, erreur)
        return None
    fiche = medias.get(media)
    if not isinstance(fiche, dict) or fiche.get('source') != 'youtube':
        return None
    yt = fiche.get('yt')
    return yt if isinstance(yt, str) and MOTIF_YOUTUBE.fullmatch(yt) else None
