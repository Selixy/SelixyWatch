import unittest

from selixy_watch.erreurs import Refus
from tests.aides_arbre import creer_noeud
from tests.aides_bdd import ADRESSE, RAISON
from tests.aides_bibliotheque import CasBibliotheque
from tests.aides_envoi import MP3, envoyer, regler_offre


@unittest.skipUnless(ADRESSE, RAISON)
class TestEnvoiRefuse(CasBibliotheque):
    def code_refus(self, offre, valide, quota):
        playlist = creer_noeud(self, "a", "P", "playlist")
        regler_offre("a", offre, valide, quota)
        with self.assertRaises(Refus) as contexte:
            envoyer("a", playlist)
        return contexte.exception.code

    def test_free_refuse_402(self):
        self.assertEqual(self.code_refus("free", True, 0), 402)

    def test_pro_sans_email_valide_403(self):
        self.assertEqual(self.code_refus("pro", False, 10**9), 403)

    def test_pro_quota_depasse_507(self):
        self.assertEqual(self.code_refus("pro", True, len(MP3) - 1), 507)
