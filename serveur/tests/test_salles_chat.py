import unittest

from selixy_watch.bdd.connexion import transaction
from selixy_watch.chat.historique import derniers
from selixy_watch.chat.messages import message
from selixy_watch.configuration import MAX_CHAT
from selixy_watch.etat import DERNIER_MESSAGE
from tests.aides_bdd import ADRESSE, RAISON
from tests.aides_salles import faux_h, monde, preparer


@unittest.skipUnless(ADRESSE, RAISON)
class TestChat(unittest.TestCase):
    def setUp(self):
        preparer(self)
        monde().close()

    def test_message_persiste_en_base(self):
        self.assertEqual(message(faux_h("bob", {"texte": "salut"}), "pl1")[0], 200)
        with transaction() as cx:
            lignes = derniers(cx, "pl1")
        self.assertEqual(len(lignes), 1)
        self.assertEqual(lignes[0]["texte"], "salut")
        self.assertEqual(lignes[0]["auteur"], {"id": "bob", "pseudo": "Bob", "avatar": None})
        self.assertEqual(set(lignes[0]), {"id", "t", "auteur", "texte"})

    def test_cent_derniers_dans_l_ordre(self):
        with transaction() as cx:
            for n in range(MAX_CHAT + 5):
                cx.execute("INSERT INTO messages (canal_id, compte_id, pseudo, texte) VALUES ('pl1', 'bob', 'Bob', %s)", (str(n),))
        with transaction() as cx:
            lignes = derniers(cx, "pl1")
        self.assertEqual([m["texte"] for m in lignes][0], "5")
        self.assertEqual(lignes[-1]["texte"], str(MAX_CHAT + 4))

    def test_auteur_supprime_garde_son_pseudo(self):
        message(faux_h("bob", {"texte": "ciao"}), "pl1")
        with transaction() as cx:
            cx.execute("DELETE FROM comptes WHERE id = 'bob'")
            self.assertEqual(derniers(cx, "pl1")[0]["auteur"]["pseudo"], "Bob")

    def test_un_message_a_la_fois(self):
        message(faux_h("bob", {"texte": "un"}), "pl1")
        self.assertIn("bob", DERNIER_MESSAGE)
        with self.assertRaises(Exception):
            message(faux_h("bob", {"texte": "deux"}), "pl1")
