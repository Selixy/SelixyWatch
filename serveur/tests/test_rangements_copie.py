import unittest

from selixy_watch.bdd.connexion import transaction
from selixy_watch.bdd.migrations import migrer
from tests.aides_arbre import creer_noeud
from tests.aides_bdd import ADRESSE, RAISON
from tests.aides_rangements import CasRangements


def requete(sql):
    with transaction() as cx:
        resultat = cx.execute(sql)
        return resultat.fetchall() if sql.startswith("SELECT") else []


@unittest.skipUnless(ADRESSE, RAISON)
class TestCopieAcceptation(CasRangements):
    def test_copie_a_l_acceptation(self):
        haut, bas, liste = self.arbre_partage()
        propre = creer_noeud(self, "b", "Mien")
        code, corps = self.inviter_et_accepter("a", "b", [haut])
        self.assertEqual((code, corps["deja"]), (200, False))
        vue = self.vue("b")
        self.assertEqual((vue[haut]["parent"], vue[bas]["parent"], vue[liste]["parent"]), ("racine", haut, bas))
        self.assertGreater(vue[haut]["rang"], vue[propre]["rang"])
        lignes = requete("SELECT noeud_id FROM rangements WHERE compte_id = 'b'")
        self.assertEqual({ligne["noeud_id"] for ligne in lignes}, {haut, bas, liste})

    def test_deplacements_du_proprietaire_sans_effet_chez_l_invite(self):
        haut, bas, liste = self.arbre_partage()
        self.inviter_et_accepter("a", "b", [haut])
        self.renommer("a", bas, "Renommé")
        self.deplacer("a", liste, haut)
        vue = self.vue("b")
        self.assertEqual((vue[bas]["nom"], vue[liste]["parent"]), ("Bas", bas))
        self.assertEqual(self.vue("a")[liste]["parent"], haut)
        self.renommer("b", bas, "Chez b")
        self.assertEqual(self.vue("a")[bas]["nom"], "Renommé")

    def test_noeud_cree_plus_tard_sous_son_parent_chez_l_invite(self):
        haut, bas, _ = self.arbre_partage()
        self.inviter_et_accepter("a", "b", [haut])
        perso = creer_noeud(self, "b", "Perso")
        self.deplacer("b", bas, perso)
        neuf = creer_noeud(self, "a", "Neuf", parent=bas)
        vue = self.vue("b")
        self.assertEqual((vue[neuf]["parent"], vue[neuf]["nom"]), (bas, "Neuf"))
        self.assertEqual(vue[bas]["parent"], perso)

    def test_migration_007_reprend_les_partages_existants(self):
        haut, bas, liste = self.arbre_partage()
        self.partager(haut, "b", "editeur")
        requete("DROP TABLE rangements")
        requete("DELETE FROM migrations WHERE version LIKE '007%'")
        with transaction() as cx:
            self.assertEqual(migrer(cx), ["007_rangements.sql"])
        lignes = {ligne["noeud_id"]: ligne for ligne in requete("SELECT * FROM rangements WHERE compte_id = 'b'")}
        self.assertEqual({k: v["parent_id"] for k, v in lignes.items()}, {haut: None, bas: haut, liste: bas})
        self.assertEqual(lignes[bas]["nom"], "Bas")
