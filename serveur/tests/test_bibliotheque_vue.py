import unittest

from tests import aides_synchro
from selixy_watch.bibliotheque.routes import route_bibliotheque
from tests.aides_arbre import ajouter_piste, creer_noeud, inserer_media
from tests.aides_bdd import ADRESSE, RAISON
from tests.aides_bibliotheque import CasBibliotheque


@unittest.skipUnless(ADRESSE, RAISON)
class TestVue(CasBibliotheque):
    def lire(self, ident):
        code, corps = self.appeler(ident, route_bibliotheque, None)
        self.assertEqual(code, 200)
        return {n["id"]: n for n in corps["noeuds"]}, corps["medias"]

    def test_anonyme_refuse(self):
        code, corps = self.appeler(None, route_bibliotheque, None)
        self.assertEqual(code, 401)

    def test_arbre_personnel(self):
        dossier = creer_noeud(self, "a", "Films")
        playlist = creer_noeud(self, "a", "Soir", "playlist", dossier)
        inserer_media("a", "m1")
        ajouter_piste(self, "a", playlist, "m1")
        noeuds, medias = self.lire("a")
        self.assertEqual(noeuds[dossier]["parent"], "racine")
        self.assertEqual(noeuds[playlist]["parent"], dossier)
        self.assertEqual(noeuds[playlist]["pistes"], ["m1"])
        self.assertEqual(noeuds[playlist]["role"], "proprietaire")
        self.assertEqual(noeuds[playlist]["proprietaire"]["id"], "a")
        self.assertIn("m1", medias)
        self.assertEqual(self.lire("b"), ({}, {}))

    def test_partages_et_roles(self):
        dossier = creer_noeud(self, "a", "Films")
        playlist = creer_noeud(self, "a", "Soir", "playlist", dossier)
        prive = creer_noeud(self, "a", "Privé")
        self.partager(dossier, "b", "editeur")
        self.partager(playlist, "c", "lecteur")
        noeuds_b, _ = self.lire("b")
        self.assertEqual(set(noeuds_b), {dossier, playlist})
        self.assertEqual(noeuds_b[dossier]["parent"], "racine")
        self.assertTrue(noeuds_b[dossier]["partage_racine"])
        self.assertFalse(noeuds_b[playlist]["partage_racine"])
        self.assertEqual(noeuds_b[dossier]["role"], "editeur")
        self.assertEqual(noeuds_b[playlist]["parent"], dossier)
        self.assertEqual(noeuds_b[playlist]["role"], "editeur")
        self.assertEqual(noeuds_b[dossier]["proprietaire"]["id"], "a")
        noeuds_c, _ = self.lire("c")
        self.assertEqual(set(noeuds_c), {playlist})
        self.assertEqual(noeuds_c[playlist]["parent"], "racine")
        self.assertEqual(noeuds_c[playlist]["role"], "lecteur")
        self.assertNotIn(prive, noeuds_b)

    def test_medias_du_partage_visibles(self):
        playlist = creer_noeud(self, "a", "Soir", "playlist")
        inserer_media("a", "m1")
        ajouter_piste(self, "a", playlist, "m1")
        self.partager(playlist, "b", "lecteur")
        _, medias = self.lire("b")
        self.assertEqual(list(medias), ["m1"])
