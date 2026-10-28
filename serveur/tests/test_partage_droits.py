import threading
import unittest

from tests.aides_partage import BancPartage

from selixy_watch.acces.droits import role_sur
from selixy_watch.bdd.connexion import transaction
from selixy_watch.partage.routes_invitation import accepter_invitation
from tests.aides_bdd import ADRESSE, RAISON
from tests.aides_invitation import creer_invitation

DOSSIER = "dossier000001"
PLAYLIST = "playlist00001"


@unittest.skipUnless(ADRESSE, RAISON)
class TestDroitsPartage(BancPartage):
    def role(self, ident, noeud):
        with transaction() as cx:
            return role_sur(cx, ident, noeud)

    def test_dossier_partage_donne_les_playlists_enfants(self):
        self.assertIsNone(self.role("b", PLAYLIST))
        self.appeler(accepter_invitation, "b", {"jeton": creer_invitation(self)["jeton"]})
        self.assertEqual(self.role("b", PLAYLIST), "editeur")

    def test_ancien_lecteur_releve_editeur(self):
        self.requete("INSERT INTO partages (noeud_id, compte_id, role) VALUES (%s, 'b', 'lecteur') RETURNING 1", (DOSSIER,))
        self.assertEqual(self.role("b", DOSSIER), "lecteur")
        corps = self.appeler(accepter_invitation, "b", {"jeton": creer_invitation(self)["jeton"]})[1]
        self.assertFalse(corps["deja"])
        self.assertEqual(self.role("b", DOSSIER), "editeur")

    def test_dernier_usage_un_seul_gagnant(self):
        jeton = creer_invitation(self, usages=1)["jeton"]
        codes = []
        cible = lambda ident: lambda: codes.append(self.appeler(accepter_invitation, ident, {"jeton": jeton})[0])
        fils = [threading.Thread(target=cible(ident)) for ident in ("b", "c")]
        for fil in fils:
            fil.start()
        for fil in fils:
            fil.join()
        self.assertEqual(sorted(codes), [200, 410])
        self.assertEqual(len(self.requete("SELECT 1 FROM partages")), 1)
        self.assertEqual(self.requete("SELECT usages FROM invitations")[0]["usages"], 1)
