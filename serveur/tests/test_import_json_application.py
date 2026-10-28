import unittest

from tests.aides_banc_import import BancImport
from tests.aides_bdd import ADRESSE, RAISON


@unittest.skipUnless(ADRESSE, RAISON)
class TestImportJsonApplication(BancImport):
    def setUp(self):
        super().setUp()
        self.code, self.texte = self.lancer("--renommer", "lntel=Lintel", "--appliquer")

    def test_comptes_herites_et_proprietaire(self):
        self.assertEqual(self.code, 0, self.texte)
        comptes = {c["id"]: c for c in self.lignes("SELECT * FROM comptes")}
        self.assertEqual(len(comptes), 4)
        self.assertTrue(all(c["mdp_hash"] is None for c in comptes.values()))
        self.assertEqual(comptes["cccccccccccccccc"]["pseudo"], "Lintel")
        self.assertEqual((comptes["aaaaaaaaaaaaaaaa"]["avatar"], comptes["aaaaaaaaaaaaaaaa"]["avatar_version"]), ("png", 3))
        self.assertEqual({n["proprietaire_id"] for n in self.lignes("SELECT * FROM noeuds")}, {"aaaaaaaaaaaaaaaa"})

    def test_arbre_et_rangs(self):
        noeuds = {n["id"]: n for n in self.lignes("SELECT * FROM noeuds")}
        self.assertIsNone(noeuds["d1"]["parent_id"])
        self.assertEqual((noeuds["p3"]["parent_id"], noeuds["p3"]["rang"]), (None, 1))
        self.assertEqual((noeuds["p2"]["parent_id"], noeuds["d2"]["rang"], noeuds["p1"]["rang"]), ("d2", 1, 0))
        self.assertEqual(int(noeuds["d1"]["cree_le"].timestamp()), 1700000000)

    def test_medias_et_pistes(self):
        medias = {m["id"]: m for m in self.lignes("SELECT * FROM medias")}
        self.assertEqual(set(medias), {"m1", "m2", "m3"})
        self.assertEqual((medias["m1"]["source"], medias["m1"]["reference_youtube"], medias["m1"]["fichier"]), ("youtube", "abc123", None))
        self.assertEqual((medias["m2"]["fichier"], medias["m2"]["taille"], medias["m2"]["miniature"]), ("m2.mp4", 1000, True))
        self.assertEqual(medias["m3"]["genre"], "audio")
        pistes = [(p["playlist_id"], p["media_id"], p["rang"]) for p in self.lignes("SELECT * FROM playlist_medias ORDER BY playlist_id, rang")]
        self.assertEqual(pistes, [("p1", "m1", 0), ("p1", "m2", 1), ("p2", "m2", 0), ("p2", "m3", 1)])

    def test_messages(self):
        messages = self.lignes("SELECT * FROM messages ORDER BY id")
        self.assertEqual([(m["compte_id"], m["pseudo"], m["texte"]) for m in messages],
                         [("dddddddddddddddd", "Camille", "salut"), (None, "Parti", "bye")])
