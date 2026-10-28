import unittest

from selixy_watch.comptes.inscription import inscription
from selixy_watch.comptes.pseudo_libre import DEJA_PRIS, RESSEMBLE
from tests.aides_bdd import ADRESSE, RAISON
from tests.aides_comptes import appeler, preparer_base


@unittest.skipUnless(ADRESSE, RAISON)
class TestHomonymes(unittest.TestCase):
    def setUp(self):
        preparer_base()
        self.assertEqual(appeler(inscription, {"pseudo": "Intel", "mdp": "motdepasse1"})[0], 201)

    def test_formes_identiques(self):
        for pseudo in ("INTEL", "intel"):
            with self.subTest(pseudo=pseudo):
                code, corps, _ = appeler(inscription, {"pseudo": pseudo, "mdp": "motdepasse1"})
                self.assertEqual((code, corps["erreur"]), (409, DEJA_PRIS))

    def test_ressemblances(self):
        for pseudo in ("lntel", "In_tel", "1ntel"):
            with self.subTest(pseudo=pseudo):
                code, corps, _ = appeler(inscription, {"pseudo": pseudo, "mdp": "motdepasse1"})
                self.assertEqual((code, corps["erreur"]), (409, RESSEMBLE))

    def test_cyrillique_refuse(self):
        code, _, _ = appeler(inscription, {"pseudo": "Іntel", "mdp": "motdepasse1"})
        self.assertIn(code, (400, 409))
        code, corps, _ = appeler(inscription, {"pseudo": "Інтел", "mdp": "motdepasse1"})
        self.assertEqual(code, 201)
