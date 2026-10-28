import os
from urllib.parse import quote

from selixy_watch.configuration import BDD_HOTE, BDD_MDP_FICHIER, BDD_NOM, BDD_PORT, BDD_UTILISATEUR


def mot_de_passe():
    with open(BDD_MDP_FICHIER, encoding="utf-8") as f:
        return f.read().strip()


def adresse():
    direct = os.environ.get("BDD_URL")
    if direct:
        return direct
    return f"postgresql://{quote(BDD_UTILISATEUR)}:{quote(mot_de_passe())}@{BDD_HOTE}:{BDD_PORT}/{BDD_NOM}"
