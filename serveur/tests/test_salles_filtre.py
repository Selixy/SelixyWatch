import queue
import unittest

from selixy_watch.canaux.ordre import etat_vide
from selixy_watch.canaux.publication import publier
from selixy_watch.etat import ABONNES, CANAUX
from selixy_watch.flux.depart import canaux_accessibles, evenements_de_depart
from tests.aides_bdd import ADRESSE, RAISON
from tests.aides_salles import monde, preparer


@unittest.skipUnless(ADRESSE, RAISON)
class TestFiltre(unittest.TestCase):
    def setUp(self):
        preparer(self)
        self.cx = monde()
        self.addCleanup(self.cx.close)
        CANAUX["pl1"] = etat_vide()

    def test_canaux_de_depart_selon_l_acces(self):
        self.assertEqual(list(canaux_accessibles(self.cx, "alice")), ["pl1"])
        self.assertEqual(list(canaux_accessibles(self.cx, "bob")), ["pl1"])
        self.assertEqual(canaux_accessibles(self.cx, "carl"), {})
        self.assertEqual(canaux_accessibles(self.cx, None), {})

    def test_depart_sans_arbre(self):
        noms = [nom for nom, _ in evenements_de_depart(self.cx, "pl1", "bob")]
        self.assertEqual(noms, ["canaux", "chat", "signal"])
        self.assertEqual([nom for nom, _ in evenements_de_depart(self.cx, None, None)], ["canaux"])

    def test_etat_envoye_aux_abonnes_et_concernes_seulement(self):
        files = {nom: queue.Queue() for nom in ("sur_canal", "invite", "etranger", "anonyme")}
        ABONNES[files["sur_canal"]] = {"canal": "pl1", "ident": "carl"}
        ABONNES[files["invite"]] = {"canal": None, "ident": "bob"}
        ABONNES[files["etranger"]] = {"canal": None, "ident": "carl"}
        ABONNES[files["anonyme"]] = {"canal": None, "ident": None}
        publier(self.cx, "pl1", CANAUX["pl1"])
        recu = {nom: not q.empty() for nom, q in files.items()}
        self.assertEqual(recu, {"sur_canal": True, "invite": True, "etranger": False, "anonyme": False})
