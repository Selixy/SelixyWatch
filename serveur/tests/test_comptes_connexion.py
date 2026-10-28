import unittest

from selixy_watch.bdd.connexion import transaction
from selixy_watch.comptes.inscription import connexion, inscription
from tests.aides_bdd import ADRESSE, RAISON
from tests.aides_comptes import appeler, preparer_base


@unittest.skipUnless(ADRESSE, RAISON)
class TestConnexion(unittest.TestCase):
    def setUp(self):
        preparer_base()
        appeler(inscription, {"pseudo": "Alice", "mdp": "motdepasse1"})

    def test_connexion_correcte_insensible_a_la_casse(self):
        code, public, entetes = appeler(connexion, {"pseudo": "ALICE", "mdp": "motdepasse1"})
        self.assertEqual(code, 200)
        self.assertEqual(public["pseudo"], "Alice")
        self.assertNotIn("active", public)
        self.assertTrue(any(v.startswith("session=") for _, v in entetes))

    def test_mauvais_mot_de_passe_et_pseudo_inconnu(self):
        self.assertEqual(appeler(connexion, {"pseudo": "Alice", "mdp": "mauvais-mdp"})[0], 401)
        self.assertEqual(appeler(connexion, {"pseudo": "Inconnu", "mdp": "motdepasse1"})[0], 401)

    def test_frein_par_pseudo_puis_par_ip(self):
        for n in range(5):
            self.assertEqual(appeler(connexion, {"pseudo": "Alice", "mdp": "mauvais-mdp"}, ip=f"10.0.0.{n}")[0], 401)
        self.assertEqual(appeler(connexion, {"pseudo": "Alice", "mdp": "motdepasse1"}, ip="10.9.9.9")[0], 429)
        for n in range(5):
            appeler(connexion, {"pseudo": f"Autre{n}", "mdp": "mauvais-mdp"}, ip="10.7.7.7")
        self.assertEqual(appeler(connexion, {"pseudo": "Alice", "mdp": "motdepasse1"}, ip="10.7.7.7")[0], 429)

    def test_compte_hérité_active_a_la_premiere_connexion(self):
        with transaction() as cx:
            cx.execute("INSERT INTO comptes (id, pseudo, pseudo_canonique, pseudo_squelette) VALUES ('h1', 'Ancien', 'ancien', 'ancien')")
        code, public, _ = appeler(connexion, {"pseudo": "Ancien", "mdp": "nouveaumdp1"})
        self.assertEqual((code, public.get("active")), (200, True))
        self.assertEqual(appeler(connexion, {"pseudo": "Ancien", "mdp": "autremdp123"})[0], 401)
        code, public, _ = appeler(connexion, {"pseudo": "Ancien", "mdp": "nouveaumdp1"})
        self.assertEqual((code, "active" in public), (200, False))
