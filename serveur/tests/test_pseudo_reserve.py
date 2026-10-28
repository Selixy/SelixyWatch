import unittest

from selixy_watch.bdd.import_json.plan import construire
from selixy_watch.comptes.pseudo import valider
from selixy_watch.erreurs import Refus


def donnees(*pseudos):
    return {"profils": {f"{i:016x}": {"pseudo": p, "avatar": None, "v": 0} for i, p in enumerate(pseudos)}, "arbre": [], "medias": {}, "chat": {}}


class TestPseudoReserve(unittest.TestCase):
    def test_reserve_refuse_par_defaut(self):
        with self.assertRaises(Refus):
            valider("Selixy")

    def test_reserve_permis_sur_demande(self):
        self.assertEqual(valider("Selixy", reserve_permis=True), "Selixy")

    def test_import_permet_le_reserve_au_seul_proprietaire(self):
        plan = construire(donnees("Selixy", "Admin"), "selixy", {}, "/nulle-part")
        self.assertEqual([c["pseudo"] for c in plan["comptes"]], ["Selixy"])
        self.assertEqual([p for _, p, _ in plan["invalides"]], ["Admin"])
