import unittest

from tests import aides_synchro
from selixy_watch.bdd.connexion import transaction
from selixy_watch.erreurs import Refus
from tests.aides_arbre import creer_noeud
from tests.aides_bdd import ADRESSE, RAISON
from tests.aides_bibliotheque import CasBibliotheque
from tests.aides_envoi import MP3, definir_quota, envoyer


@unittest.skipUnless(ADRESSE, RAISON)
class TestEnvoi(CasBibliotheque):
    def test_envoi_appartient_a_l_expediteur(self):
        playlist = creer_noeud(self, "a", "P", "playlist")
        self.partager(playlist, "b", "editeur")
        definir_quota("b", 10**6)
        code, media = envoyer("b", playlist)
        self.assertEqual((code, media["nom"]), (201, "Chanson"))
        with transaction() as cx:
            ligne = cx.execute("SELECT proprietaire_id FROM medias WHERE id = %s", (media["id"],)).fetchone()
        self.assertEqual(ligne["proprietaire_id"], "b")
        self.playlist_modifiee.assert_called()

    def test_quota(self):
        playlist = creer_noeud(self, "a", "P", "playlist")
        definir_quota("a", len(MP3) + 10)
        self.assertEqual(envoyer("a", playlist)[0], 201)
        with self.assertRaises(Refus) as contexte:
            envoyer("a", playlist)
        self.assertEqual(contexte.exception.code, 507)

    def test_envoi_refuse_au_lecteur(self):
        playlist = creer_noeud(self, "a", "P", "playlist")
        self.partager(playlist, "b", "lecteur")
        with self.assertRaises(Refus) as contexte:
            envoyer("b", playlist)
        self.assertEqual(contexte.exception.code, 403)
