import unittest

from selixy_watch.comptes.confirmation import confirmer
from selixy_watch.comptes.courriel_compte import definir_email, supprimer_email
from tests.aides_bdd import ADRESSE, RAISON
from tests.aides_comptes import appeler
from tests.aides_courriel import MDP, inscrire, jeton_du_dernier_mail, ligne_compte, preparer_courriel, valider_email


@unittest.skipUnless(ADRESSE, RAISON)
class TestAdressesEmail(unittest.TestCase):
    def setUp(self):
        preparer_courriel()
        self.session = inscrire("Alice")

    def test_adresse_prise_et_suppression(self):
        valider_email(self.session, "a@b.fr")
        autre = inscrire("Bob")
        self.assertEqual(appeler(definir_email, {"email": "A@B.fr", "mdp": MDP}, jeton=autre)[0], 409)
        appeler(definir_email, {"email": "x@y.fr", "mdp": MDP}, jeton=autre)
        jeton = jeton_du_dernier_mail()
        valider_email(self.session, "x@y.fr")
        self.assertEqual(appeler(confirmer, {"jeton": jeton})[0], 409)
        self.assertEqual(appeler(supprimer_email, {"mdp": MDP}, jeton=self.session)[0], 200)
        self.assertIsNone(ligne_compte("Alice")["email"])
        self.assertEqual(appeler(definir_email, {"email": "x@y.fr", "mdp": MDP}, jeton=autre)[0], 200)

    def test_frein_cinq_envois_par_heure(self):
        codes = [appeler(definir_email, {"email": f"a{i}@b.fr", "mdp": MDP}, jeton=self.session)[0] for i in range(6)]
        self.assertEqual(codes, [200] * 5 + [429])
