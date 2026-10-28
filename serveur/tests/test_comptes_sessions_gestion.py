import unittest

from selixy_watch.bdd.connexion import transaction
from selixy_watch.comptes.inscription import connexion, inscription
from selixy_watch.comptes.moi import moi
from selixy_watch.comptes.sessions_gestion import lister, revoquer
from tests.aides_bdd import ADRESSE, RAISON
from tests.aides_comptes import FauxGestionnaire, appeler, jeton_de_reponse, preparer_base


@unittest.skipUnless(ADRESSE, RAISON)
class TestGestionDesSessions(unittest.TestCase):
    def setUp(self):
        preparer_base()
        self.premiere = jeton_de_reponse(appeler(inscription, {"pseudo": "Alice", "mdp": "motdepasse1"}))
        appeler(connexion, {"pseudo": "Alice", "mdp": "motdepasse1"})

    def test_lister_revoquer_et_prolongation(self):
        code, corps = lister(FauxGestionnaire(jeton=self.premiere), None)
        self.assertEqual(code, 200)
        self.assertEqual(sorted(s["courante"] for s in corps["sessions"]), [False, True])
        autre = next(s["id"] for s in corps["sessions"] if not s["courante"])
        appeler(revoquer, {"id": autre}, jeton=self.premiere)
        self.assertEqual(len(lister(FauxGestionnaire(jeton=self.premiere), None)[1]["sessions"]), 1)
        with transaction() as cx:
            cx.execute("UPDATE sessions SET expire_le = now() + interval '2 days'")
        reponse = moi(FauxGestionnaire(jeton=self.premiere), None)
        self.assertEqual(reponse[1]["pseudo"], "Alice")
        self.assertTrue(reponse[2])
