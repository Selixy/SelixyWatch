import unittest

from tests.aides_partage import BancPartage

from selixy_watch.partage.routes_invitation import accepter_invitation
from tests.aides_bdd import ADRESSE, RAISON
from tests.aides_invitation import creer_invitation

USAGES = "SELECT usages FROM invitations"
EXPIRER = "UPDATE invitations SET expire_le = now() - interval '1 day' RETURNING 1"


@unittest.skipUnless(ADRESSE, RAISON)
class TestAcceptation(BancPartage):
    def test_accepter_cree_le_partage_et_consomme(self):
        jeton = creer_invitation(self)["jeton"]
        code, corps = self.appeler(accepter_invitation, "b", {"jeton": jeton})
        self.assertEqual((code, corps["deja"], "editeur"), (200, False, "editeur"))
        self.assertEqual(self.requete("SELECT compte_id, role FROM partages"), [{"compte_id": "b", "role": "editeur"}])
        self.assertEqual((self.requete(USAGES)[0]["usages"], self.signaux), (1, [{"b"}]))

    def test_reaccepter_ne_consomme_pas(self):
        jeton = creer_invitation(self)["jeton"]
        self.appeler(accepter_invitation, "b", {"jeton": jeton})
        code, corps = self.appeler(accepter_invitation, "b", {"jeton": jeton})
        self.assertEqual((code, corps["deja"], self.requete(USAGES)[0]["usages"]), (200, True, 1))

    def test_epuisee_mais_deja_abonne(self):
        jeton = creer_invitation(self, usages=1)["jeton"]
        self.appeler(accepter_invitation, "b", {"jeton": jeton})
        self.assertTrue(self.appeler(accepter_invitation, "b", {"jeton": jeton})[1]["deja"])
        self.assertEqual(self.appeler(accepter_invitation, "c", {"jeton": jeton})[0], 410)

    def test_expiree(self):
        jeton = creer_invitation(self)["jeton"]
        self.requete(EXPIRER)
        self.assertEqual(self.appeler(accepter_invitation, "b", {"jeton": jeton})[0], 410)
        self.assertEqual(self.requete("SELECT 1 FROM partages"), [])

    def test_proprietaire_ne_s_invite_pas(self):
        jeton = creer_invitation(self)["jeton"]
        self.requete(EXPIRER)
        code, corps = self.appeler(accepter_invitation, "a", {"jeton": jeton})
        self.assertEqual((code, corps["deja"], self.requete(USAGES)[0]["usages"]), (200, True, 0))
        self.assertEqual(self.requete("SELECT 1 FROM partages"), [])
