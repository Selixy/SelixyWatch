import unittest
from unittest.mock import patch

from tests import aides_synchro
from tests.aides_arbre import creer_noeud
from tests.aides_bdd import ADRESSE, RAISON
from tests.aides_bibliotheque import CasBibliotheque


@unittest.skipUnless(ADRESSE, RAISON)
class TestSignalement(CasBibliotheque):
    def test_concernes_d_une_creation_chez_un_invite(self):
        dossier = creer_noeud(self, "a", "Films")
        self.partager(dossier, "b", "lecteur")
        self.partager(dossier, "c", "editeur")
        with patch("selixy_watch.arbre.actions.signaler") as signaler:
            creer_noeud(self, "c", "Sous", parent=dossier)
        self.assertEqual(signaler.call_args.args[0], {"a", "b", "c"})
