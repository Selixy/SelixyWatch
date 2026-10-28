import unittest

from psycopg.errors import ForeignKeyViolation

from selixy_watch.bdd.migrations import migrer, versions_disponibles
from tests.aides_bdd import ADRESSE, RAISON, compte, connexion_vierge


@unittest.skipUnless(ADRESSE, RAISON)
class TestMigrations(unittest.TestCase):
    def setUp(self):
        self.connexion = connexion_vierge()

    def tearDown(self):
        self.connexion.close()

    def test_applique_tout_puis_ne_fait_plus_rien(self):
        self.assertEqual(migrer(self.connexion), versions_disponibles())
        self.connexion.commit()
        self.assertEqual(migrer(self.connexion), [])

    def test_media_retenu_par_une_playlist(self):
        migrer(self.connexion)
        compte(self.connexion, "a", "Intel", "intel", "intel")
        self.connexion.execute("INSERT INTO noeuds (id, proprietaire_id, type, nom) VALUES ('p', 'a', 'playlist', 'P')")
        self.connexion.execute("INSERT INTO medias (id, proprietaire_id, source, nom) VALUES ('m', 'a', 'fichier', 'M')")
        self.connexion.execute("INSERT INTO playlist_medias (playlist_id, media_id, rang) VALUES ('p', 'm', 0)")
        with self.assertRaises(ForeignKeyViolation):
            self.connexion.execute("DELETE FROM medias WHERE id = 'm'")
