import unittest

from selixy_watch.administration.principal import executer
from selixy_watch.bdd.connexion import transaction
from tests.aides_bdd import ADRESSE, RAISON
from tests.aides_courriel import inscrire, ligne_compte, preparer_courriel, valider_email

GO = 1024 ** 3


@unittest.skipUnless(ADRESSE, RAISON)
class TestAdministrationOffre(unittest.TestCase):
    def setUp(self):
        preparer_courriel()
        self.session = inscrire("Alice")

    def lancer(self, *argv):
        return executer(list(argv), transaction)

    def test_pro_refuse_sans_email_valide(self):
        code, texte = self.lancer("pro", "Alice")
        self.assertEqual(code, 1)
        self.assertIn("e-mail", texte)
        self.assertEqual(ligne_compte("Alice")["offre"], "free")

    def test_pro_free_quota_et_lister(self):
        valider_email(self.session, "alice@exemple.fr")
        self.assertEqual(self.lancer("pro", "alice")[0], 0)
        compte = ligne_compte("Alice")
        self.assertEqual((compte["offre"], compte["quota_octets"]), ("pro", 20 * GO))
        self.lancer("quota", "Alice", "5")
        self.assertEqual(ligne_compte("Alice")["quota_octets"], 5 * GO)
        self.assertIn("pro", self.lancer("lister")[1])
        self.lancer("pro", "Alice", "--quota-go", "50")
        self.assertEqual(ligne_compte("Alice")["quota_octets"], 50 * GO)
        self.lancer("free", "Alice")
        compte = ligne_compte("Alice")
        self.assertEqual((compte["offre"], compte["quota_octets"]), ("free", 0))
        self.assertEqual(self.lancer("free", "Inconnu")[0], 1)
