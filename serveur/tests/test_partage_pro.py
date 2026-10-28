import unittest

from selixy_watch.partage.routes_invitation import accepter_invitation, inviter, voir
from tests.aides_bdd import ADRESSE, RAISON
from tests.aides_partage import BancPartage

DOSSIER = ["dossier000001"]


@unittest.skipUnless(ADRESSE, RAISON)
class TestInvitationPro(BancPartage):
    def lien_pro(self):
        self.requete("UPDATE comptes SET admin = true WHERE id = 'a' RETURNING 1")
        return self.appeler(inviter, "a", {"noeuds": DOSSIER, "pro": True})[1]["jeton"]

    def test_seul_un_admin_offre_pro(self):
        self.assertEqual(self.appeler(inviter, "a", {"noeuds": DOSSIER, "pro": True})[0], 403)
        self.assertEqual(self.requete("SELECT 1 FROM invitations"), [])

    def test_acceptation_donne_pro_et_acces(self):
        jeton = self.lien_pro()
        self.assertTrue(self.appeler(voir, None, {"jeton": jeton})[1]["pro"])
        corps = self.appeler(accepter_invitation, "b", {"jeton": jeton})[1]
        self.assertEqual((corps["deja"], corps["pro"]), (False, True))
        compte = self.requete("SELECT offre, quota_octets FROM comptes WHERE id = 'b'")[0]
        self.assertEqual((compte["offre"], compte["quota_octets"]), ("pro", 20 * 1024 ** 3))

    def test_acces_deja_present_donne_quand_meme_pro(self):
        self.requete("INSERT INTO partages (noeud_id, compte_id, role) VALUES ('dossier000001', 'b', 'editeur') RETURNING 1")
        corps = self.appeler(accepter_invitation, "b", {"jeton": self.lien_pro()})[1]
        self.assertEqual((corps["deja"], corps["pro"]), (False, True))
        self.assertEqual(self.requete("SELECT usages FROM invitations")[0]["usages"], 1)

    def test_ephemere_et_lien_ordinaire_sans_pro(self):
        self.requete("UPDATE comptes SET ephemere = true WHERE id = 'c' RETURNING 1")
        self.assertFalse(self.appeler(accepter_invitation, "c", {"jeton": self.lien_pro()})[1]["pro"])
        jeton = self.appeler(inviter, "a", {"noeuds": ["playlist00002"]})[1]["jeton"]
        self.assertFalse(self.appeler(accepter_invitation, "b", {"jeton": jeton})[1]["pro"])
        self.assertEqual(self.requete("SELECT offre FROM comptes WHERE id IN ('b', 'c') ORDER BY id"), [{"offre": "free"}, {"offre": "free"}])
