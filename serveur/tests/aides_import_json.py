import json
import os
import tempfile
from contextlib import contextmanager

PROFILS = {
    "aaaaaaaaaaaaaaaa": {"pseudo": "Marion_", "avatar": "png", "v": 3},
    "bbbbbbbbbbbbbbbb": {"pseudo": "Intel", "avatar": None, "v": 0},
    "cccccccccccccccc": {"pseudo": "lntel", "avatar": "jpg", "v": 2},
    "dddddddddddddddd": {"pseudo": "Camille", "avatar": None, "v": 0},
}
ARBRE = [
    {"id": "d1", "parent": "racine", "type": "dossier", "nom": "Films", "t": 1700000000},
    {"id": "p1", "parent": "d1", "type": "playlist", "nom": "Soirée", "t": 1700000100, "pistes": ["m1", "m2", "inconnu"]},
    {"id": "d2", "parent": "d1", "type": "dossier", "nom": "Vieux", "t": 1700000200},
    {"id": "p2", "parent": "d2", "type": "playlist", "nom": "Musique", "t": 1700000300, "pistes": ["m2", "m3"]},
    {"id": "p3", "parent": "racine", "type": "playlist", "nom": "Vide", "t": 1700000400, "pistes": []},
]
MEDIAS = {
    "m1": {"nom": "Clip", "genre": "video", "source": "youtube", "yt": "abc123", "duree": 61.5, "t": 1700000010},
    "m2": {"nom": "Film", "genre": "video", "ext": "mp4", "taille": 1000, "mini": True, "duree": 90, "t": 1700000020},
    "m3": {"nom": "Chanson", "genre": "audio", "ext": "mp3", "taille": 50, "duree": 180, "t": 1700000030},
    "m4": {"nom": "Orphelin", "genre": "video", "ext": "mp4", "taille": 5, "duree": 1, "t": 1700000040},
}
CHAT = {
    "p1": [
        {"id": "x1", "t": 1700000500, "auteur": {"id": "dddddddddddddddd", "pseudo": "Camille", "avatar": None}, "texte": "salut"},
        {"id": "x2", "t": 1700000600, "auteur": {"id": "zzzz", "pseudo": "Parti", "avatar": None}, "texte": "bye"},
    ],
    "disparu": [{"id": "x3", "t": 1700000700, "auteur": {"id": "aaaaaaaaaaaaaaaa", "pseudo": "Marion_"}, "texte": "perdu"}],
}


def ecrire_jeu(dossier):
    for nom, contenu in (("profils", PROFILS), ("arbre", ARBRE), ("medias", MEDIAS), ("chat", CHAT)):
        with open(os.path.join(dossier, f"{nom}.json"), "w", encoding="utf-8") as f:
            json.dump(contenu, f)
    os.makedirs(os.path.join(dossier, "medias"))
    for nom in ("m2.mp4",):
        open(os.path.join(dossier, "medias", nom), "wb").close()


def jeu_json():
    dossier = tempfile.mkdtemp()
    ecrire_jeu(dossier)
    return dossier


def fabrique_transaction(connexion):
    @contextmanager
    def transaction():
        try:
            yield connexion
        except BaseException:
            connexion.rollback()
            raise
        connexion.commit()

    return transaction
