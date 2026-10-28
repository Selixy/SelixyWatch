import unittest

from tests.aides_partage import BancPartage

from selixy_watch.partage.routes_gestion import revoquer
from selixy_watch.partage.routes_invitation import accepter_invitation
from tests.aides_bdd import ADRESSE, RAISON
from tests.aides_invitation import BancAvecInvite

DOSSIER = "dossier000001"


@unittest.skipUnless(ADRESSE, RAISON)
class TestRevocation(BancAvecInvite):
    def test_revoquer_invitation(self):
        corps = {"invitation": self.invitation["id"]}
        self.assertEqual(self.appeler(revoquer, "b", corps, DOSSIER)[0], 403)
        self.assertEqual(self.appeler(revoquer, "a", corps, DOSSIER)[0], 200)
        self.assertEqual(self.appeler(accepter_invitation, "c", {"jeton": self.invitation["jeton"]})[0], 404)
        self.assertEqual(self.requete("SELECT 1 FROM invitation_noeuds"), [])
