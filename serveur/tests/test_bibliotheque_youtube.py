import unittest

from tests import aides_synchro
from selixy_watch.arbre.routes import route_arbre
from selixy_watch.bdd.connexion import transaction
from selixy_watch.liens.suivi import SuiviImport
from tests.aides_arbre import creer_noeud
from tests.aides_bdd import ADRESSE, RAISON
from tests.aides_bibliotheque import CasBibliotheque


@unittest.skipUnless(ADRESSE, RAISON)
class TestYoutube(CasBibliotheque):
    def medias(self):
        with transaction() as cx:
            return cx.execute("SELECT proprietaire_id, reference_youtube FROM medias ORDER BY proprietaire_id").fetchall()

    def test_dedoublonnage_par_proprietaire(self):
        un = creer_noeud(self, "a", "Un", "playlist")
        deux = creer_noeud(self, "a", "Deux", "playlist")
        suivi = SuiviImport(un, "a")
        suivi.ajouter("abcdefghijk", "Titre", 100.0)
        suivi.ajouter("abcdefghijk", "Titre", 100.0)
        SuiviImport(deux, "a").ajouter("abcdefghijk", "Titre", 100.0)
        self.assertEqual(suivi.ajoutes, 1)
        self.assertEqual(len(self.medias()), 1)

    def test_media_au_compte_qui_importe(self):
        playlist = creer_noeud(self, "a", "P", "playlist")
        self.partager(playlist, "b", "editeur")
        SuiviImport(playlist, "b").ajouter("abcdefghijk", "Titre", 100.0)
        SuiviImport(playlist, "a").ajouter("abcdefghijk", "Titre", 100.0)
        self.assertEqual([(m["proprietaire_id"], m["reference_youtube"]) for m in self.medias()], [("a", "abcdefghijk"), ("b", "abcdefghijk")])

    def test_import_refuse_sans_droit_d_edition(self):
        playlist = creer_noeud(self, "a", "P", "playlist")
        self.partager(playlist, "b", "lecteur")
        suivi = SuiviImport(playlist, "b")
        suivi.ajouter("abcdefghijk", "Titre", 100.0)
        self.assertEqual((suivi.ajoutes, self.medias()), (0, []))

    def test_suppression_de_playlist_efface_les_medias(self):
        playlist = creer_noeud(self, "a", "P", "playlist")
        SuiviImport(playlist, "a").ajouter("abcdefghijk", "Titre", 100.0)
        self.appeler("a", route_arbre, "supprimer", corps={"id": playlist})
        self.assertEqual(self.medias(), [])
        self.playlist_supprimee.assert_called_once_with(playlist)
