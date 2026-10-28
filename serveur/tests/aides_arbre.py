from tests import aides_synchro
from selixy_watch.arbre.routes import route_arbre
from selixy_watch.bdd.connexion import transaction
from selixy_watch.playlist.routes import route_playlist


def creer_noeud(cas, ident, nom, type_="dossier", parent="racine"):
    code, corps = cas.appeler(ident, route_arbre, "creer", corps={"nom": nom, "type": type_, "parent": parent})
    cas.assertEqual(code, 200)
    return corps["id"]


def inserer_media(proprietaire, mid, taille=0, fichier=None):
    with transaction() as cx:
        cx.execute(
            "INSERT INTO medias (id, proprietaire_id, source, nom, genre, duree, fichier, taille) VALUES (%s, %s, %s, %s, 'audio', 10, %s, %s)",
            (mid, proprietaire, "fichier" if fichier else "youtube", f"Média {mid}", fichier, taille),
        )


def ajouter_piste(cas, ident, pid, mid, avant=None):
    return cas.appeler(ident, route_playlist, pid, "ajouter", corps={"media": mid, "avant": avant})


def ordre_enfants(parent, proprietaire="a"):
    with transaction() as cx:
        lignes = cx.execute(
            "SELECT id FROM noeuds WHERE parent_id IS NOT DISTINCT FROM %s AND proprietaire_id = %s ORDER BY rang", (parent, proprietaire)
        )
        return [ligne["id"] for ligne in lignes]
