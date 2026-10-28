import unittest

from tests.aides_arbre import creer_noeud
from tests.aides_bdd import ADRESSE, RAISON
from tests.aides_bibliotheque import CasBibliotheque
from tests.aides_envoi import envoyer, regler_offre


@unittest.skipUnless(ADRESSE, RAISON)
class TestEnvoiProValide(CasBibliotheque):
    def test_pro_valide_accepte(self):
        playlist = creer_noeud(self, "a", "P", "playlist")
        regler_offre("a", "pro", True, 10**9)
        self.assertEqual(envoyer("a", playlist)[0], 201)
