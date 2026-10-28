import json
import os
import tempfile

from selixy_watch.configuration import DOSSIER


def lire_json(nom, defaut):
    try:
        with open(os.path.join(DOSSIER, nom), encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return defaut


def ecrire_json(nom, donnees, mode=0o600):
    os.makedirs(DOSSIER, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=DOSSIER)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(donnees, f, ensure_ascii=False)
    os.chmod(tmp, mode)
    os.replace(tmp, os.path.join(DOSSIER, nom))


def ecrire_fichier_public(chemin, donnees):
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    with open(chemin, "wb") as f:
        f.write(donnees)
    os.chmod(chemin, 0o644)
