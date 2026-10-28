import unittest

from selixy_watch.bdd.connexion import transaction
from selixy_watch.comptes.inscription import connexion
from selixy_watch.comptes.recuperation import changer, demander
from selixy_watch.comptes.session import ident
from selixy_watch.courriel import envoi
from tests.aides_bdd import ADRESSE, RAISON
from tests.aides_comptes import FauxGestionnaire, appeler, jeton_de_reponse
from tests.aides_courriel import MDP, inscrire, jeton_du_dernier_mail, preparer_courriel, valider_email


@unittest.skipUnless(ADRESSE, RAISON)
class TestRecuperation(unittest.TestCase):
    def setUp(self):
        preparer_courriel()
        self.session = inscrire("Alice")
        valider_email(self.session, "alice@exemple.fr")
        envoi.BOITE_MEMOIRE.clear()

    def test_meme_reponse_et_mail_seulement_si_valide(self):
        inscrire("Bob")
        reponses = [appeler(demander, {"identifiant": i}) for i in ("Alice", "alice@exemple.fr", "inconnu", "Bob")]
        self.assertTrue(all(r[:2] == (200, {"ok": 1}) for r in reponses))
        self.assertEqual([m["destinataire"] for m in envoi.BOITE_MEMOIRE], ["alice@exemple.fr"] * 2)

    def test_changement_de_mot_de_passe_et_sessions(self):
        autre = jeton_de_reponse(appeler(connexion, {"pseudo": "Alice", "mdp": MDP}))
        appeler(demander, {"identifiant": "alice"})
        reponse = appeler(changer, {"jeton": jeton_du_dernier_mail(), "mdp": "nouveau-mdp-9"})
        self.assertEqual((reponse[0], reponse[1]["pseudo"]), (200, "Alice"))
        nouvelle = jeton_de_reponse(reponse)
        self.assertIsNone(ident(FauxGestionnaire(jeton=self.session)))
        self.assertIsNone(ident(FauxGestionnaire(jeton=autre)))
        self.assertIsNotNone(ident(FauxGestionnaire(jeton=nouvelle)))
        self.assertEqual(appeler(connexion, {"pseudo": "Alice", "mdp": MDP})[0], 401)
        self.assertEqual(appeler(connexion, {"pseudo": "Alice", "mdp": "nouveau-mdp-9"})[0], 200)

    def test_jeton_unique_expire_ou_adresse_changee(self):
        appeler(demander, {"identifiant": "alice"})
        jeton = jeton_du_dernier_mail()
        self.assertEqual(appeler(changer, {"jeton": jeton, "mdp": "court"})[0], 400)
        self.assertEqual(appeler(changer, {"jeton": jeton, "mdp": "nouveau-mdp-9"})[0], 200)
        self.assertEqual(appeler(changer, {"jeton": jeton, "mdp": "nouveau-mdp-9"})[0], 410)
        appeler(demander, {"identifiant": "alice"})
        jeton = jeton_du_dernier_mail()
        with transaction() as cx:
            cx.execute("UPDATE comptes SET email = 'autre@exemple.fr'")
        self.assertEqual(appeler(changer, {"jeton": jeton, "mdp": "nouveau-mdp-9"})[0], 410)

    def test_frein_par_identifiant(self):
        codes = [appeler(demander, {"identifiant": "inconnu"}, ip=f"10.0.1.{i}")[0] for i in range(6)]
        self.assertEqual(codes, [200] * 5 + [429])
