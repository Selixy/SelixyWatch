import unittest

from psycopg.errors import UniqueViolation

from selixy_watch.bdd.migrations import migrer
from tests.aides_bdd import ADRESSE, RAISON, compte, connexion_vierge


@unittest.skipUnless(ADRESSE, RAISON)
class TestPseudosUniques(unittest.TestCase):
    def setUp(self):
        self.connexion = connexion_vierge()
        migrer(self.connexion)
        compte(self.connexion, "a", "Intel", "intel", "intel")

    def tearDown(self):
        self.connexion.close()

    def test_canonique_unique(self):
        with self.assertRaises(UniqueViolation):
            compte(self.connexion, "b", "INTEL", "intel", "inteI")

    def test_squelette_unique(self):
        with self.assertRaises(UniqueViolation):
            compte(self.connexion, "b", "In_tel", "in_tel", "intel")
