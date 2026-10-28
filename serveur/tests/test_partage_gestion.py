import types
import unittest
import urllib.parse

from tests.aides_partage import faux_gestionnaire

from selixy_watch.partage.routes_gestion import lire, quitter, retirer
from tests.aides_bdd import ADRESSE, RAISON
from tests.aides_invitation import BancAvecInvite

DOSSIER = "dossier000001"
PLAYLIST = "playlist00001"


@unittest.skipUnless(ADRESSE, RAISON)
class TestGestionPartage(BancAvecInvite):
    def test_lire_reserve_au_proprietaire(self):
        url = types.SimpleNamespace(query=urllib.parse.urlencode({"noeud": DOSSIER}))
        code, corps = lire(faux_gestionnaire("a", {}), url)
        self.assertEqual(code, 200)
        self.assertEqual(corps["invites"], [{"compte": {"id": "b", "pseudo": "pseudo_b", "avatar": None}}])
        self.assertEqual(corps["invitations"][0]["noeuds"], [{"id": DOSSIER, "nom": DOSSIER}])
        self.assertEqual((corps["invitations"][0]["usages"], lire(faux_gestionnaire("b", {}), url)[0]), (1, 403))

    def test_retirer_signale_avant_suppression(self):
        self.assertEqual(self.appeler(retirer, "b", {"compte": "b"}, DOSSIER)[0], 403)
        self.assertEqual(self.appeler(retirer, "a", {"compte": "b"}, DOSSIER)[0], 200)
        self.assertEqual((self.requete("SELECT 1 FROM partages"), self.signaux), ([], [{"a", "b"}]))

    def test_quitter_seulement_a_la_racine_du_partage(self):
        self.assertEqual(self.appeler(quitter, "b", {}, PLAYLIST)[0], 400)
        self.assertEqual(self.appeler(quitter, "a", {}, DOSSIER)[0], 400)
        self.assertEqual(self.appeler(quitter, "b", {}, DOSSIER)[0], 200)
        self.assertEqual((self.requete("SELECT 1 FROM partages"), self.signaux), ([], [{"a", "b"}]))
