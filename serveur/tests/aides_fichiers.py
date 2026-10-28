import os
import sys
import types

from selixy_watch.configuration import DOSSIER_MEDIAS


INSERT_MEDIA = "INSERT INTO medias (id, proprietaire_id, source, nom, fichier, taille) VALUES (%s, %s, 'fichier', 'm', %s, 1)"


def creer_fichiers(*noms):
    os.makedirs(DOSSIER_MEDIAS, exist_ok=True)
    for nom in noms:
        with open(os.path.join(DOSSIER_MEDIAS, nom), "wb") as f:
            f.write(b"x")


def existe(nom):
    return os.path.exists(os.path.join(DOSSIER_MEDIAS, nom))


def installer_faux_signal(cas):
    signaux = []
    faux = types.ModuleType("selixy_watch.diffusion.bibliotheque")
    faux.signaler = signaux.append
    ancien = sys.modules.get("selixy_watch.diffusion.bibliotheque")
    sys.modules["selixy_watch.diffusion.bibliotheque"] = faux

    def restaurer():
        sys.modules.pop("selixy_watch.diffusion.bibliotheque", None)
        if ancien:
            sys.modules["selixy_watch.diffusion.bibliotheque"] = ancien

    cas.addCleanup(restaurer)
    return signaux
