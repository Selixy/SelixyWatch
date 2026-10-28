import unittest

from tests import aides_synchro
from selixy_watch.arbre.routes import route_arbre
from selixy_watch.bdd.connexion import transaction
from tests.aides_arbre import creer_noeud
from tests.aides_bdd import ADRESSE, RAISON
from tests.aides_bibliotheque import CasBibliotheque


@unittest.skipUnless(ADRESSE, RAISON)
class TestDroits(CasBibliotheque):
    def setUp(self):
        super().setUp()
        self.dossier = creer_noeud(self, "a", "Films")
        self.partager(self.dossier, "b", "lecteur")
        self.partager(self.dossier, "c", "editeur")

    def test_lecteur_ne_modifie_pas(self):
        self.assertEqual(self.refus("b", route_arbre, "creer", corps={"parent": self.dossier, "nom": "X", "type": "dossier"}), 403)
        self.assertEqual(self.refus("b", route_arbre, "supprimer", corps={"id": self.dossier}), 403)

    def test_editeur_modifie_et_cree_chez_le_proprietaire(self):
        sous = creer_noeud(self, "c", "Sous", parent=self.dossier)
        code, _ = self.appeler("c", route_arbre, "renommer", corps={"id": self.dossier, "nom": "Renommé"})
        self.assertEqual(code, 200)
        with transaction() as cx:
            ligne = cx.execute("SELECT proprietaire_id, nom FROM noeuds WHERE id = %s", (sous,)).fetchone()
            nom = cx.execute("SELECT nom FROM noeuds WHERE id = %s", (self.dossier,)).fetchone()["nom"]
        self.assertEqual(ligne["proprietaire_id"], "a")
        self.assertEqual(nom, "Films")
        self.appeler("c", route_arbre, "supprimer", corps={"id": sous})

    def test_inconnu_et_anonyme(self):
        self.assertEqual(self.refus("b", route_arbre, "renommer", corps={"id": "inexistant00", "nom": "X"}), 404)
        prive = creer_noeud(self, "a", "Privé")
        self.assertEqual(self.refus("b", route_arbre, "supprimer", corps={"id": prive}), 404)
        self.assertEqual(self.refus(None, route_arbre, "creer", corps={"nom": "X"}), 401)

    def test_racine_de_partage_non_supprimable(self):
        self.assertEqual(self.refus("c", route_arbre, "supprimer", corps={"id": self.dossier}), 403)
        code, _ = self.appeler("a", route_arbre, "supprimer", corps={"id": self.dossier})
        self.assertEqual(code, 200)
