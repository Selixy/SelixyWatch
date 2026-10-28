import unittest

from selixy_watch.bdd.connexion import transaction
from selixy_watch.comptes.confirmation import confirmer
from selixy_watch.comptes.courriel_compte import definir_email
from selixy_watch.comptes.moi import moi
from selixy_watch.courriel import envoi
from tests.aides_bdd import ADRESSE, RAISON
from tests.aides_comptes import FauxGestionnaire, appeler
from tests.aides_courriel import MDP, inscrire, jeton_du_dernier_mail, preparer_courriel


@unittest.skipUnless(ADRESSE, RAISON)
class TestConfirmationEmail(unittest.TestCase):
    def setUp(self):
        preparer_courriel()
        self.session = inscrire("Alice")

    def test_en_attente_puis_confirme(self):
        reponse = appeler(definir_email, {"email": "Alice@Exemple.fr", "mdp": MDP}, jeton=self.session)
        self.assertEqual(reponse[:2], (200, {"envoye": True}))
        self.assertEqual(envoi.BOITE_MEMOIRE[-1]["destinataire"], "alice@exemple.fr")
        avant = moi(FauxGestionnaire(jeton=self.session), None)[1]
        self.assertEqual((avant["email"], avant["email_valide"], avant["email_en_attente"]), (None, False, "alice@exemple.fr"))
        self.assertEqual(appeler(confirmer, {"jeton": jeton_du_dernier_mail()})[:2], (200, {"email": "alice@exemple.fr"}))
        apres = moi(FauxGestionnaire(jeton=self.session), None)[1]
        self.assertEqual((apres["email"], apres["email_valide"], apres["email_en_attente"]), ("alice@exemple.fr", True, None))
        self.assertEqual((apres["offre"], apres["envoi_fichiers"], apres["quota"]), ("free", False, 0))

    def test_mot_de_passe_adresse_et_ephemere(self):
        self.assertEqual(appeler(definir_email, {"email": "a@b.fr", "mdp": "faux-faux"}, jeton=self.session)[0], 401)
        self.assertEqual(appeler(definir_email, {"email": "pas-une-adresse", "mdp": MDP}, jeton=self.session)[0], 400)
        self.assertEqual(appeler(definir_email, {"email": "a@b.fr", "mdp": MDP})[0], 401)
        with transaction() as cx:
            cx.execute("UPDATE comptes SET ephemere = true")
        self.assertEqual(appeler(definir_email, {"email": "a@b.fr", "mdp": MDP}, jeton=self.session)[0], 403)

    def test_jeton_reutilise_ou_expire(self):
        appeler(definir_email, {"email": "a@b.fr", "mdp": MDP}, jeton=self.session)
        jeton = jeton_du_dernier_mail()
        self.assertEqual(appeler(confirmer, {"jeton": jeton})[0], 200)
        self.assertEqual(appeler(confirmer, {"jeton": jeton})[0], 410)
        appeler(definir_email, {"email": "c@d.fr", "mdp": MDP}, jeton=self.session)
        jeton = jeton_du_dernier_mail()
        with transaction() as cx:
            cx.execute("UPDATE jetons_courriel SET expire_le = now() - interval '1 minute'")
        self.assertEqual(appeler(confirmer, {"jeton": jeton})[0], 410)
        self.assertEqual(appeler(confirmer, {"jeton": 12})[0], 410)
