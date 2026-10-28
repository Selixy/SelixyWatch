import unittest

from selixy_watch.arbre.routes import route_arbre
from tests.aides_arbre import creer_noeud
from tests.aides_bdd import ADRESSE, RAISON
from tests.aides_rangements import CasRangements


@unittest.skipUnless(ADRESSE, RAISON)
class TestRangementsPerso(CasRangements):
    def test_repli_sur_le_reel(self):
        haut, bas, liste = self.arbre_partage()
        self.partager(haut, "b", "editeur")
        vue = self.vue("b")
        self.assertEqual((vue[haut]["parent"], vue[bas]["parent"], vue[liste]["parent"]), ("racine", haut, bas))
        self.assertEqual(vue[bas]["nom"], "Bas")

    def test_deplacement_perso_invisible_aux_autres(self):
        haut, bas, _ = self.arbre_partage()
        self.partager(haut, "b", "editeur")
        self.partager(haut, "c", "editeur")
        perso = creer_noeud(self, "b", "Perso")
        self.assertEqual(self.deplacer("b", bas, perso)[0], 200)
        self.assertEqual(self.vue("b")[bas]["parent"], perso)
        self.assertEqual(self.vue("a")[bas]["parent"], haut)
        self.assertEqual(self.vue("c")[bas]["parent"], haut)

    def test_renommage_perso(self):
        haut, _, _ = self.arbre_partage()
        self.partager(haut, "b", "lecteur")
        self.assertEqual(self.renommer("b", haut, "Mon nom")[0], 200)
        self.assertEqual(self.vue("b")[haut]["nom"], "Mon nom")
        self.assertEqual(self.vue("a")[haut]["nom"], "Haut")
        self.renommer("a", haut, "Nom du patron")
        self.assertEqual(self.vue("b")[haut]["nom"], "Mon nom")
        self.assertEqual(self.vue("a")[haut]["nom"], "Nom du patron")

    def test_deplacer_dans_mon_dossier_puis_retour(self):
        haut, _, _ = self.arbre_partage()
        self.partager(haut, "b", "editeur")
        perso = creer_noeud(self, "b", "Perso")
        self.deplacer("b", haut, perso)
        vue = self.vue("b")
        self.assertEqual((vue[haut]["parent"], vue[haut]["partage_racine"]), (perso, True))
        self.deplacer("b", haut, "racine")
        self.assertEqual(self.vue("b")[haut]["parent"], "racine")
