import unittest
from unittest.mock import patch

from selixy_watch.canaux.occupation import auto_demarrer, auto_mettre_en_pause, canal_occupe
from selixy_watch.etat import ABONNES, CANAUX
from tests.aides_bdd import ADRESSE, RAISON
from tests.aides_salles import monde, preparer


@unittest.skipUnless(ADRESSE, RAISON)
class TestOccupation(unittest.TestCase):
    def setUp(self):
        preparer(self)
        self.cx = monde()
        self.addCleanup(self.cx.close)

    def test_canal_occupe(self):
        self.assertFalse(canal_occupe("pl1"))
        ABONNES["q1"] = {"canal": "autre", "ident": "u1"}
        self.assertFalse(canal_occupe("pl1"))
        ABONNES["q2"] = {"canal": "pl1", "ident": "u2"}
        self.assertTrue(canal_occupe("pl1"))

    def test_auto_demarrer_inoccupe(self):
        auto_demarrer(self.cx, "pl1")
        e = CANAUX.get("pl1")
        self.assertTrue(e["lecture"])
        self.assertEqual(e["courant"], "m1")

    def test_auto_demarrer_avance_si_fini(self):
        CANAUX["pl1"] = {"courant": "m1", "lecture": False, "pos": 100.0, "t0": 0.0, "v": 1, "boucle": False, "aleatoire": False, "melange": []}
        auto_demarrer(self.cx, "pl1")
        self.assertTrue(CANAUX["pl1"]["lecture"])
        self.assertEqual(CANAUX["pl1"]["courant"], "m2")

    def test_auto_mettre_en_pause(self):
        ABONNES["q1"] = {"canal": "pl1", "ident": "u1"}
        CANAUX["pl1"] = {"courant": "m1", "lecture": True, "pos": 10.0, "t0": 1000.0, "v": 1, "boucle": False, "aleatoire": False, "melange": []}
        auto_mettre_en_pause(self.cx, "pl1")
        self.assertTrue(CANAUX["pl1"]["lecture"])
        ABONNES.clear()
        with patch("time.time", return_value=1005.0):
            auto_mettre_en_pause(self.cx, "pl1")
        self.assertFalse(CANAUX["pl1"]["lecture"])
        self.assertEqual(CANAUX["pl1"]["pos"], 15.0)
