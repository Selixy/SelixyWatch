import os
import unittest

from tests import aides_synchro
from selixy_watch import configuration
from selixy_watch.bdd.connexion import transaction
from selixy_watch.playlist.routes import route_playlist
from tests.aides_arbre import ajouter_piste, creer_noeud, inserer_media
from tests.aides_bdd import ADRESSE, RAISON
from tests.aides_bibliotheque import CasBibliotheque
from tests.aides_envoi import definir_quota, envoyer

@unittest.skipUnless(ADRESSE, RAISON)
class TestMedias(CasBibliotheque):
    def test_orphelins_supprimes_avec_fichiers(self):
        playlist = creer_noeud(self, "a", "P", "playlist")
        definir_quota("a", 10**6)
        _, media = envoyer("a", playlist)
        chemin = os.path.join(configuration.DOSSIER_MEDIAS, f"{media['id']}.mp3")
        self.assertTrue(os.path.exists(chemin))
        self.appeler("a", route_playlist, playlist, "retirer", corps={"media": media["id"]})
        self.assertFalse(os.path.exists(chemin))
        with transaction() as cx:
            self.assertIsNone(cx.execute("SELECT 1 FROM medias WHERE id = %s", (media["id"],)).fetchone())
        self.avant_retrait.assert_called_once()

    def test_doublon_et_visibilite(self):
        playlist = creer_noeud(self, "a", "P", "playlist")
        inserer_media("a", "m1")
        ajouter_piste(self, "a", playlist, "m1")
        self.assertEqual(self.refus("a", route_playlist, playlist, "ajouter", corps={"media": "m1"}), 409)
        autre = creer_noeud(self, "b", "Autre", "playlist")
        self.assertEqual(self.refus("b", route_playlist, autre, "ajouter", corps={"media": "m1"}), 404)
        self.partager(playlist, "b", "lecteur")
        self.assertEqual(ajouter_piste(self, "b", autre, "m1")[0], 200)
