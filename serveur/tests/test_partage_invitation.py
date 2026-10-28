import unittest

from tests.aides_partage import BancPartage

from selixy_watch.partage.jetons import hacher
from selixy_watch.partage.routes_invitation import accepter_invitation, inviter, voir
from tests.aides_bdd import ADRESSE, RAISON

DOSSIER = "dossier000001"


@unittest.skipUnless(ADRESSE, RAISON)
class TestInvitation(BancPartage):
    def test_seul_le_proprietaire_invite(self):
        self.assertEqual(self.appeler(inviter, "b", {"noeuds": [DOSSIER]})[0], 404)
        self.assertEqual(self.appeler(inviter, None, {"noeuds": [DOSSIER]})[0], 401)
        code, corps = self.appeler(inviter, "a", {"noeuds": [DOSSIER]})
        self.assertEqual(code, 201)
        self.assertEqual(corps["lien"], f"/invitation/#{corps['jeton']}")
        self.assertEqual((len(corps["id"]), corps["noeuds"]), (12, [{"id": DOSSIER, "type": "dossier", "nom": DOSSIER}]))

    def test_seul_le_hash_est_stocke_et_role_unique(self):
        corps = self.appeler(inviter, "a", {"noeuds": [DOSSIER]})[1]
        lignes = self.requete("SELECT jeton_hash, usages_max, role FROM invitations")
        self.assertEqual(lignes, [{"jeton_hash": hacher(corps["jeton"]), "usages_max": 5, "role": "editeur"}])

    def test_bornes_refusees(self):
        for corps in ({}, {"noeuds": []}, {"noeuds": [DOSSIER, DOSSIER]}, {"noeuds": [DOSSIER], "usages_max": 51}, {"noeuds": [DOSSIER], "jours": 0}):
            self.assertEqual(self.appeler(inviter, "a", corps)[0], 400, corps)

    def test_voir_anonyme(self):
        jeton = self.appeler(inviter, "a", {"noeuds": [DOSSIER]})[1]["jeton"]
        code, corps = self.appeler(voir, None, {"jeton": jeton})
        self.assertEqual(code, 200)
        self.assertEqual(corps["noeuds"], [{"id": DOSSIER, "type": "dossier", "nom": DOSSIER}])
        self.assertEqual((corps["valide"], corps["par"]["pseudo"]), (True, "pseudo_a"))
        self.assertEqual(self.appeler(voir, None, {"jeton": "inconnu"})[0], 404)

    def test_accepter_non_connecte(self):
        jeton = self.appeler(inviter, "a", {"noeuds": [DOSSIER]})[1]["jeton"]
        self.assertEqual(self.appeler(accepter_invitation, None, {"jeton": jeton})[0], 401)
