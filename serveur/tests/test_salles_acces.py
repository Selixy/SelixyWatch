import unittest

from selixy_watch.canaux.route import commande_canal
from selixy_watch.chat.messages import message
from selixy_watch.erreurs import Refus
from selixy_watch.etat import CANAUX
from selixy_watch.vocal.signal import signal
from tests.aides_bdd import ADRESSE, RAISON
from tests.aides_salles import faux_h, monde, preparer


@unittest.skipUnless(ADRESSE, RAISON)
class TestAccesSalles(unittest.TestCase):
    def setUp(self):
        preparer(self)
        monde().close()

    def code_refus(self, fonction, *args):
        with self.assertRaises(Refus) as ctx:
            fonction(*args)
        return ctx.exception.code

    def test_anonyme_refuse_partout(self):
        self.assertEqual(self.code_refus(commande_canal, faux_h(None), "pl1", "lire"), 401)
        self.assertEqual(self.code_refus(message, faux_h(None, {"texte": "a"}), "pl1"), 401)
        self.assertEqual(self.code_refus(signal, faux_h(None, {"action": "etat"}), "pl1"), 401)

    def test_non_invite_refuse_partout(self):
        self.assertEqual(self.code_refus(commande_canal, faux_h("alice"), "zz1", "lire"), 404)
        self.assertEqual(self.code_refus(commande_canal, faux_h("carl"), "pl1", "lire"), 404)
        self.assertEqual(self.code_refus(message, faux_h("carl", {"texte": "a"}), "pl1"), 404)
        self.assertEqual(self.code_refus(signal, faux_h("carl", {"action": "etat"}), "pl1"), 404)
        self.assertNotIn("pl1", CANAUX)

    def test_invite_lecteur_commande_la_room(self):
        self.assertEqual(commande_canal(faux_h("bob"), "pl1", "lire")[0], 200)
        self.assertEqual(CANAUX["pl1"]["courant"], "m1")
        self.assertEqual(signal(faux_h("bob", {"action": "etat", "data": {"micro": True}}), "pl1")[0], 200)
