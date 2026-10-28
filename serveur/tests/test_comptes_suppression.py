import os
import unittest

from selixy_watch.bdd.connexion import transaction
from selixy_watch.comptes.avatar import avatar
from selixy_watch.comptes.inscription import inscription
from selixy_watch.comptes.moi import renommer
from selixy_watch.comptes.suppression import supprimer
from selixy_watch.configuration import DOSSIER_AVATARS, DOSSIER_MEDIAS
from selixy_watch.diffusion.presence import presence
from selixy_watch.etat import ABONNES
from tests.aides_bdd import ADRESSE, RAISON
from tests.aides_comptes import FauxGestionnaire, appeler, jeton_de_reponse, preparer_base

PNG = b"\x89PNG\r\n\x1a\n" + b"0" * 20


@unittest.skipUnless(ADRESSE, RAISON)
class TestSuppressionEtProfils(unittest.TestCase):
    def setUp(self):
        preparer_base()
        os.makedirs(DOSSIER_MEDIAS, exist_ok=True)
        reponse = appeler(inscription, {"pseudo": "Alice", "mdp": "motdepasse1"})
        self.compte, self.jeton = reponse[1]["id"], jeton_de_reponse(reponse)

    def test_avatar_puis_presence(self):
        reponse = avatar(FauxGestionnaire(brut=PNG, jeton=self.jeton))
        self.assertEqual(reponse[1]["avatar"], f"/avatars/{self.compte}.png?v=1")
        self.assertTrue(os.path.exists(os.path.join(DOSSIER_AVATARS, f"{self.compte}.png")))
        ABONNES["q"] = {"canal": "c1", "ident": self.compte}
        try:
            self.assertEqual(presence()["canaux"]["c1"][0]["pseudo"], "Alice")
        finally:
            ABONNES.pop("q")

    def test_renommage_conserve_les_regles(self):
        appeler(inscription, {"pseudo": "Bob", "mdp": "motdepasse1"})
        self.assertEqual(appeler(renommer, {"pseudo": "bob"}, jeton=self.jeton)[0], 409)
        self.assertEqual(appeler(renommer, {"pseudo": "ALICE"}, jeton=self.jeton)[0], 200)

    def test_suppression_du_compte_et_des_fichiers(self):
        avatar(FauxGestionnaire(brut=PNG, jeton=self.jeton))
        fichier = os.path.join(DOSSIER_MEDIAS, "aaaaaaaaaaaa.mp4")
        mini = os.path.join(DOSSIER_MEDIAS, "aaaaaaaaaaaa-mini.jpg")
        for chemin in (fichier, mini):
            with open(chemin, "wb") as f:
                f.write(b"x")
        with transaction() as cx:
            cx.execute("INSERT INTO medias (id, proprietaire_id, source, nom, fichier, taille) VALUES ('aaaaaaaaaaaa', %s, 'fichier', 'm', 'aaaaaaaaaaaa.mp4', 1)", (self.compte,))
            cx.execute("INSERT INTO noeuds (id, proprietaire_id, type, nom) VALUES ('nnnnnnnnnnnn', %s, 'playlist', 'p')", (self.compte,))
            cx.execute("INSERT INTO playlist_medias (playlist_id, media_id, rang) VALUES ('nnnnnnnnnnnn', 'aaaaaaaaaaaa', 0)")
        self.assertEqual(appeler(supprimer, {"mdp": "faux-mot-de-passe"}, jeton=self.jeton)[0], 401)
        self.assertEqual(appeler(supprimer, {"mdp": "motdepasse1"}, jeton=self.jeton)[0], 200)
        self.assertFalse(os.path.exists(fichier) or os.path.exists(mini))
        self.assertFalse(os.path.exists(os.path.join(DOSSIER_AVATARS, f"{self.compte}.png")))
        with transaction() as cx:
            for table in ("comptes", "sessions", "medias", "noeuds"):
                self.assertEqual(cx.execute(f"SELECT count(*) AS n FROM {table}").fetchone()["n"], 0)
