import json
import os

from selixy_watch.bdd.import_json.erreurs import ErreurImportJson

FICHIERS = (("arbre", "arbre.json", []), ("medias", "medias.json", {}), ("profils", "profils.json", {}), ("chat", "chat.json", {}))


def lire_un(dossier, nom, defaut):
    chemin = os.path.join(dossier, nom)
    if not os.path.exists(chemin):
        return defaut
    try:
        with open(chemin, encoding="utf-8") as f:
            return json.load(f)
    except ValueError as e:
        raise ErreurImportJson(f"{nom} illisible : {e}")


def lire_dossier(dossier):
    if not os.path.isdir(dossier):
        raise ErreurImportJson(f"Dossier introuvable : {dossier}")
    donnees = {cle: lire_un(dossier, nom, defaut) for cle, nom, defaut in FICHIERS}
    if not donnees["profils"]:
        raise ErreurImportJson("profils.json absent ou vide : aucun compte à importer.")
    return donnees
