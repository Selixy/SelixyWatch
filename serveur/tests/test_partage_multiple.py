import unittest

from tests.aides_partage import BancPartage

from selixy_watch.partage.routes_invitation import accepter_invitation, inviter, voir
from tests.aides_bdd import ADRESSE, RAISON
from tests.aides_invitation import creer_invitation

TROIS = ("dossier000001", "playlist00001", "playlist00002")


@unittest.skipUnless(ADRESSE, RAISON)
class TestInvitationMultiple(BancPartage):
    def test_trois_noeuds_acceptes_puis_deja(self):
        jeton = creer_invitation(self, TROIS)["jeton"]
        code, corps = self.appeler(accepter_invitation, "b", {"jeton": jeton})
        self.assertEqual((code, corps["deja"], len(corps["noeuds"])), (200, False, 3))
        self.assertEqual(len(self.requete("SELECT 1 FROM partages WHERE role = 'editeur'")), 3)
        self.assertEqual(self.requete("SELECT usages FROM invitations")[0]["usages"], 1)
        self.requete("UPDATE invitations SET expire_le = now() - interval '1 day' RETURNING 1")
        corps = self.appeler(accepter_invitation, "b", {"jeton": jeton})[1]
        self.assertEqual((corps["deja"], self.requete("SELECT usages FROM invitations")[0]["usages"]), (True, 1))

    def test_noeud_d_autrui_refuse_sans_rien_creer(self):
        self.assertEqual(self.appeler(inviter, "a", {"noeuds": [TROIS[0], "playlistdeb01"]})[0], 404)
        self.assertEqual(self.appeler(inviter, "a", {"noeuds": [TROIS[0], "inconnu00000"]})[0], 404)
        self.assertEqual(self.requete("SELECT 1 FROM invitations"), [])
        self.assertEqual(self.requete("SELECT 1 FROM invitation_noeuds"), [])

    def test_noeud_supprime_omis_puis_tous_supprimes(self):
        jeton = creer_invitation(self, TROIS[1:])["jeton"]
        self.requete("DELETE FROM noeuds WHERE id = 'playlist00002' RETURNING 1")
        noeuds = self.appeler(voir, None, {"jeton": jeton})[1]["noeuds"]
        self.assertEqual([n["id"] for n in noeuds], ["playlist00001"])
        self.requete("DELETE FROM noeuds WHERE id = 'playlist00001' RETURNING 1")
        self.assertEqual(self.appeler(voir, None, {"jeton": jeton})[0], 404)
        self.assertEqual(self.appeler(accepter_invitation, "b", {"jeton": jeton})[0], 404)

    def test_acces_partiel_cree_l_autre_et_consomme(self):
        self.requete("INSERT INTO partages (noeud_id, compte_id, role) VALUES ('playlist00001', 'b', 'editeur') RETURNING 1")
        jeton = creer_invitation(self, TROIS[1:])["jeton"]
        corps = self.appeler(accepter_invitation, "b", {"jeton": jeton})[1]
        self.assertFalse(corps["deja"])
        self.assertEqual(sorted(p["noeud_id"] for p in self.requete("SELECT noeud_id FROM partages")), ["playlist00001", "playlist00002"])
        self.assertEqual((self.requete("SELECT usages FROM invitations")[0]["usages"], self.signaux), (1, [{"b"}]))
