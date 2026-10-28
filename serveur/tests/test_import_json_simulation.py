import unittest

from tests.aides_banc_import import BancImport
from tests.aides_bdd import ADRESSE, RAISON


@unittest.skipUnless(ADRESSE, RAISON)
class TestImportJsonSimulation(BancImport):
    def test_collision_signalee_et_rien_ecrit(self):
        code, texte = self.lancer()
        self.assertEqual(code, 0)
        self.assertIn("COLLISION", texte)
        self.assertIn("'Intel'", texte)
        self.assertIn("'lntel'", texte)
        self.assertIn("REFUSE", texte)
        tables = self.connexion.execute("SELECT to_regclass('comptes') AS t").fetchone()["t"]
        self.assertIsNone(tables)

    def test_rapport_orphelins_inconnus_et_fichiers_manquants(self):
        _, texte = self.lancer("--renommer", "lntel=Lintel")
        self.assertIn("Aucun blocage", texte)
        self.assertIn("orphelin (aucune playlist), ignoré : m4", texte)
        self.assertIn("absent de medias.json, ignorée : inconnu", texte)
        self.assertIn("manquant sur disque : m3.mp3", texte)
        self.assertNotIn("manquant sur disque : m2.mp4", texte)
        self.assertIn("Messages ignorés (canal sans playlist) : 1", texte)
        self.assertIn("comptes : 4", texte)
        self.assertIn("playlist_medias : 4", texte)

    def test_application_refusee_tant_que_collision(self):
        code, texte = self.lancer("--appliquer")
        self.assertEqual(code, 1)
        self.assertIn("REFUSE", texte)

    def test_proprietaire_inconnu_et_renommage_inutile(self):
        _, texte = self.lancer("--renommer", "fantome=Autre")
        self.assertIn("Renommage inutile", texte)
        code, _ = self.lancer("--renommer", "fantome=Autre", "--appliquer")
        self.assertEqual(code, 1)

    def test_base_non_vide_refusee(self):
        self.lancer("--renommer", "lntel=Lintel", "--appliquer")
        code, texte = self.lancer("--renommer", "lntel=Lintel", "--appliquer")
        self.assertEqual(code, 1)
        self.assertIn("déjà des données", texte)
        self.assertEqual(len(self.lignes("SELECT * FROM comptes")), 4)
