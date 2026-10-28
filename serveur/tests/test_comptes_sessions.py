import unittest

from selixy_watch.bdd.connexion import transaction
from selixy_watch.comptes.inscription import connexion, inscription
from selixy_watch.comptes.moi import changer_mdp
from selixy_watch.comptes.session import hacher_jeton, ident
from selixy_watch.comptes.sessions_gestion import deconnexion, deconnexion_partout
from tests.aides_bdd import ADRESSE, RAISON
from tests.aides_comptes import FauxGestionnaire, appeler, connecte, jeton_de_reponse, preparer_base


@unittest.skipUnless(ADRESSE, RAISON)
class TestSessions(unittest.TestCase):
    def setUp(self):
        preparer_base()
        self.premiere = jeton_de_reponse(appeler(inscription, {"pseudo": "Alice", "mdp": "motdepasse1"}))
        self.seconde = jeton_de_reponse(appeler(connexion, {"pseudo": "Alice", "mdp": "motdepasse1"}))

    def test_changement_de_mdp_revoque_les_autres_sessions(self):
        code = appeler(changer_mdp, {"ancien": "motdepasse1", "nouveau": "nouveaumdp12"}, jeton=self.premiere)[0]
        self.assertEqual(code, 200)
        self.assertIsNotNone(connecte(self.premiere))
        self.assertIsNone(connecte(self.seconde))
        self.assertEqual(appeler(changer_mdp, {"ancien": "faux-ancien", "nouveau": "nouveaumdp12"}, jeton=self.premiere)[0], 401)

    def test_deconnexion_simple_et_partout(self):
        appeler(deconnexion, jeton=self.premiere)
        self.assertIsNone(connecte(self.premiere))
        self.assertIsNotNone(connecte(self.seconde))
        appeler(deconnexion_partout, jeton=self.seconde)
        self.assertIsNone(connecte(self.seconde))
        self.assertEqual(appeler(deconnexion_partout)[0], 401)

    def test_session_expiree_refusee(self):
        with transaction() as cx:
            cx.execute("UPDATE sessions SET expire_le = now() - interval '1 second' WHERE jeton_hash = %s", (hacher_jeton(self.premiere),))
        self.assertIsNone(connecte(self.premiere))
        self.assertIsNone(connecte("jeton-inconnu"))
        self.assertIsNotNone(connecte(self.seconde))

    def test_ancien_cookie_et_cache_par_requete(self):
        self.assertIsNone(ident(FauxGestionnaire(cookie_brut="mu=abcdef0123456789")))
        h = FauxGestionnaire(jeton=self.premiere)
        self.assertIsNotNone(ident(h))
        with transaction() as cx:
            cx.execute("DELETE FROM sessions")
        self.assertIsNotNone(ident(h))
