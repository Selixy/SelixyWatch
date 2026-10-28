import unittest

from selixy_watch.bdd.connexion import transaction
from selixy_watch.comptes.anonyme import anonyme
from selixy_watch.comptes.inscription import connexion, inscription
from selixy_watch.comptes.moi import changer_mdp, moi
from selixy_watch.comptes.nettoyage import purger_ephemeres_expires
from selixy_watch.comptes.session import hacher_jeton
from tests.aides_bdd import ADRESSE, RAISON
from tests.aides_comptes import FauxGestionnaire, appeler, connecte, jeton_de_reponse, preparer_base
from tests.aides_fichiers import installer_faux_signal


@unittest.skipUnless(ADRESSE, RAISON)
class TestEphemeres(unittest.TestCase):
    def setUp(self):
        preparer_base()
        self.signaux = installer_faux_signal(self)
        reponse = appeler(anonyme)
        self.compte, self.jeton = reponse[1]["id"], jeton_de_reponse(reponse)

    def test_compte_invite_utilisable_mais_sans_mot_de_passe(self):
        info = moi(FauxGestionnaire(jeton=self.jeton), None)[1]
        self.assertTrue(info["ephemere"])
        self.assertRegex(info["pseudo"], r"^Invité-\d{4}$")
        self.assertEqual(appeler(connexion, {"pseudo": info["pseudo"], "mdp": "motdepasse1"})[0], 401)
        self.assertEqual(appeler(changer_mdp, {"ancien": "motdepasse1", "nouveau": "motdepasse2"}, jeton=self.jeton)[0], 403)
        appeler(inscription, {"pseudo": "Alice", "mdp": "motdepasse1"})
        self.assertFalse(moi(FauxGestionnaire(jeton=jeton_de_reponse(appeler(connexion, {"pseudo": "Alice", "mdp": "motdepasse1"}))), None)[1]["ephemere"])

    def test_nettoyage_des_expires(self):
        vivant = jeton_de_reponse(appeler(anonyme))
        with transaction() as cx:
            cx.execute("UPDATE sessions SET expire_le = now() - interval '1 hour' WHERE jeton_hash = %s", (hacher_jeton(self.jeton),))
            cx.execute("INSERT INTO comptes (id, pseudo, pseudo_canonique, pseudo_squelette) VALUES ('perm', 'Perm', 'perm', 'perm')")
            purger_ephemeres_expires(cx)
            restants = {ligne["id"] for ligne in cx.execute("SELECT id FROM comptes")}
        self.assertNotIn(self.compte, restants)
        self.assertIn("perm", restants)
        self.assertEqual(len(restants), 2)
        self.assertIsNotNone(connecte(vivant))

    def test_frein_de_creation_par_ip(self):
        codes = [appeler(anonyme, ip="10.5.5.5")[0] for _ in range(21)]
        self.assertEqual(codes[:20], [201] * 20)
        self.assertEqual(codes[20], 429)
        self.assertEqual(appeler(anonyme, ip="10.6.6.6")[0], 201)
