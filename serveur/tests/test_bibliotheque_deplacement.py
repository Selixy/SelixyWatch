import unittest

from tests import aides_synchro
from selixy_watch.arbre.routes import route_arbre
from tests.aides_arbre import creer_noeud, ordre_enfants
from tests.aides_bdd import ADRESSE, RAISON
from tests.aides_bibliotheque import CasBibliotheque


@unittest.skipUnless(ADRESSE, RAISON)
class TestDeplacement(CasBibliotheque):
    def test_ordre_avant(self):
        un, deux, trois = (creer_noeud(self, "a", nom) for nom in ("1", "2", "3"))
        self.assertEqual(ordre_enfants(None), [un, deux, trois])
        self.appeler("a", route_arbre, "deplacer", corps={"id": trois, "vers": "racine", "avant": un})
        self.assertEqual(ordre_enfants(None), [trois, un, deux])
        self.appeler("a", route_arbre, "deplacer", corps={"id": trois, "vers": "racine"})
        self.assertEqual(ordre_enfants(None), [un, deux, trois])
        self.assertEqual(self.refus("a", route_arbre, "deplacer", corps={"id": un, "vers": "racine", "avant": un}), 400)

    def test_dans_soi_meme_et_cycle(self):
        haut = creer_noeud(self, "a", "Haut")
        bas = creer_noeud(self, "a", "Bas", parent=haut)
        self.assertEqual(self.refus("a", route_arbre, "deplacer", corps={"id": haut, "vers": haut}), 400)
        self.assertEqual(self.refus("a", route_arbre, "deplacer", corps={"id": haut, "vers": bas}), 400)

    def test_limite_de_profondeur(self):
        parent = "racine"
        for niveau in range(8):
            parent = creer_noeud(self, "a", f"n{niveau}", parent=parent)
        self.assertEqual(self.refus("a", route_arbre, "creer", corps={"parent": parent, "nom": "trop", "type": "dossier"}), 507)
        autre = creer_noeud(self, "a", "Autre")
        self.assertEqual(self.refus("a", route_arbre, "deplacer", corps={"id": autre, "vers": parent}), 400)

    def test_deplacer_dans_un_dossier(self):
        dossier = creer_noeud(self, "a", "D")
        playlist = creer_noeud(self, "a", "P", "playlist")
        code, _ = self.appeler("a", route_arbre, "deplacer", corps={"id": playlist, "vers": dossier})
        self.assertEqual(code, 200)
        self.assertEqual(ordre_enfants(dossier), [playlist])
        self.assertEqual(self.refus("a", route_arbre, "deplacer", corps={"id": dossier, "vers": playlist}), 400)
