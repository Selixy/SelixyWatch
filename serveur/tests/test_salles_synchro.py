import queue
import unittest

from selixy_watch.canaux.ordre import etat_vide
from selixy_watch.canaux.synchro import avant_retrait, playlist_modifiee, playlist_supprimee
from selixy_watch.etat import ABONNES, CANAUX
from tests.aides_bdd import ADRESSE, RAISON
from tests.aides_salles import monde, preparer


@unittest.skipUnless(ADRESSE, RAISON)
class TestSynchro(unittest.TestCase):
    def setUp(self):
        preparer(self)
        self.cx = monde()
        self.addCleanup(self.cx.close)
        CANAUX["pl1"] = {**etat_vide(), "courant": "m1", "lecture": True}

    def test_retrait_du_courant_passe_au_suivant(self):
        avant_retrait(self.cx, "pl1", "m2")
        self.assertEqual(CANAUX["pl1"]["courant"], "m1")
        avant_retrait(self.cx, "pl1", "m1")
        self.assertEqual(CANAUX["pl1"]["courant"], "m2")
        self.assertEqual(CANAUX["pl1"]["v"], 1)

    def test_retrait_du_dernier_arrete(self):
        self.cx.execute("DELETE FROM playlist_medias WHERE media_id = 'm2'")
        avant_retrait(self.cx, "pl1", "m1")
        self.assertIsNone(CANAUX["pl1"]["courant"])
        self.assertFalse(CANAUX["pl1"]["lecture"])

    def test_modification_courant_disparu_arrete_et_diffuse(self):
        q = queue.Queue()
        ABONNES[q] = {"canal": "pl1", "ident": "alice"}
        self.cx.execute("DELETE FROM playlist_medias WHERE media_id = 'm1'")
        playlist_modifiee(self.cx, "pl1")
        self.assertIsNone(CANAUX["pl1"]["courant"])
        nom, donnees = q.get_nowait()
        self.assertEqual((nom, donnees["id"]), ("canal", "pl1"))
        self.assertEqual(donnees["etat"]["suite"], ["m2"])

    def test_suppression_oublie_le_canal(self):
        playlist_supprimee("pl1")
        self.assertNotIn("pl1", CANAUX)
