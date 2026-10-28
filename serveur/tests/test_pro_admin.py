import unittest

from selixy_watch.administration.principal import executer
from selixy_watch.bdd.connexion import transaction
from selixy_watch.erreurs import Refus
from selixy_watch.comptes.moi import moi
from tests.aides_arbre import creer_noeud
from tests.aides_bdd import ADRESSE, RAISON
from tests.aides_bibliotheque import CasBibliotheque
from tests.aides_courriel import inscrire, ligne_compte, preparer_courriel, valider_email
from tests.aides_comptes import appeler
from tests.aides_envoi import envoyer, regler_offre


@unittest.skipUnless(ADRESSE, RAISON)
class TestEnvoiAdmin(CasBibliotheque):
    def test_admin_sans_limite_de_quota(self):
        playlist = creer_noeud(self, "a", "P", "playlist")
        regler_offre("a", "free", True, 0)
        with transaction() as cx:
            cx.execute("UPDATE comptes SET admin = true WHERE id = 'a'")
        self.assertEqual(envoyer("a", playlist)[0], 201)

    def test_admin_sans_email_valide_refuse(self):
        playlist = creer_noeud(self, "a", "P", "playlist")
        regler_offre("a", "free", False, 0)
        with transaction() as cx:
            cx.execute("UPDATE comptes SET admin = true WHERE id = 'a'")
        with self.assertRaises(Refus) as contexte:
            envoyer("a", playlist)
        self.assertEqual(contexte.exception.code, 403)


@unittest.skipUnless(ADRESSE, RAISON)
class TestCommandesAdmin(unittest.TestCase):
    def setUp(self):
        preparer_courriel()
        self.session = inscrire("Alice")

    def lancer(self, *argv):
        return executer(list(argv), transaction)

    def test_admin_retirer_lister_et_moi(self):
        self.assertEqual(self.lancer("admin", "alice")[0], 0)
        self.assertTrue(ligne_compte("Alice")["admin"])
        self.assertIn("admin", self.lancer("lister")[1])
        corps = appeler(lambda h: moi(h, None), jeton=self.session)[1]
        self.assertEqual((corps["admin"], corps["quota"]), (True, None))
        self.assertEqual(self.lancer("retirer-admin", "Alice")[0], 0)
        self.assertFalse(ligne_compte("Alice")["admin"])
        self.assertFalse(appeler(lambda h: moi(h, None), jeton=self.session)[1]["admin"])
        self.assertEqual(self.lancer("admin", "Inconnu")[0], 1)
