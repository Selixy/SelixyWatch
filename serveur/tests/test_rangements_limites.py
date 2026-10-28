import unittest

from selixy_watch.arbre.routes import route_arbre
from tests.aides_arbre import creer_noeud
from tests.aides_bdd import ADRESSE, RAISON
from tests.aides_rangements import CasRangements


@unittest.skipUnless(ADRESSE, RAISON)
class TestRangementsLimites(CasRangements):
    def test_cycle_et_profondeur_dans_ma_vue(self):
        haut, bas, _ = self.arbre_partage()
        self.partager(haut, "b", "editeur")
        perso = creer_noeud(self, "b", "Perso")
        self.deplacer("b", haut, perso)
        self.assertEqual(self.refus("b", route_arbre, "deplacer", corps={"id": perso, "vers": bas}), 400)
        parent = "racine"
        for niveau in range(7):
            parent = creer_noeud(self, "b", f"n{niveau}", parent=parent)
        self.assertEqual(self.refus("b", route_arbre, "deplacer", corps={"id": haut, "vers": parent}), 400)
        self.assertEqual(self.deplacer("a", bas, "racine")[0], 200)

    def test_suppression_de_mon_dossier_remonte_l_element_partage(self):
        haut, _, _ = self.arbre_partage()
        self.partager(haut, "b", "editeur")
        perso = creer_noeud(self, "b", "Perso")
        self.deplacer("b", haut, perso)
        self.assertEqual(self.appeler("b", route_arbre, "supprimer", corps={"id": perso})[0], 200)
        vue = self.vue("b")
        self.assertNotIn(perso, vue)
        self.assertEqual(vue[haut]["parent"], "racine")
