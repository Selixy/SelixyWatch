import unittest

from selixy_watch.bdd.connexion import transaction
from selixy_watch.comptes.anonyme import anonyme
from selixy_watch.comptes.inscription import inscription
from selixy_watch.comptes.sessions_gestion import deconnexion
from tests.aides_bdd import ADRESSE, RAISON
from tests.aides_comptes import FauxGestionnaire, appeler, connecte, jeton_de_reponse, preparer_base
from tests.aides_fichiers import INSERT_MEDIA, creer_fichiers, existe, installer_faux_signal


@unittest.skipUnless(ADRESSE, RAISON)
class TestPurge(unittest.TestCase):
    def setUp(self):
        preparer_base()
        self.signaux = installer_faux_signal(self)
        reponse = appeler(anonyme)
        self.compte, self.jeton = reponse[1]["id"], jeton_de_reponse(reponse)

    def test_deconnexion_purge_et_transfert(self):
        autre = appeler(inscription, {"pseudo": "Bob", "mdp": "motdepasse1"})[1]["id"]
        creer_fichiers("seul.mp4", "seul00000000-mini.jpg", "partage.mp4", "bob.mp4")
        with transaction() as cx:
            cx.execute("INSERT INTO noeuds (id, proprietaire_id, type, nom) VALUES ('mienne00000', %s, 'playlist', 'a')", (self.compte,))
            cx.execute("INSERT INTO noeuds (id, proprietaire_id, type, nom) VALUES ('bobliste000', %s, 'playlist', 'b')", (autre,))
            cx.execute(INSERT_MEDIA, ("seul00000000", self.compte, "seul.mp4"))
            cx.execute(INSERT_MEDIA, ("partage00000", self.compte, "partage.mp4"))
            cx.execute(INSERT_MEDIA, ("bob000000000", autre, "bob.mp4"))
            cx.execute("INSERT INTO playlist_medias (playlist_id, media_id, rang) VALUES ('mienne00000', 'seul00000000', 0), ('mienne00000', 'bob000000000', 1), ('bobliste000', 'partage00000', 0)")
            cx.execute("INSERT INTO partages (noeud_id, compte_id, role) VALUES ('mienne00000', %s, 'lecteur')", (autre,))
        self.assertEqual(deconnexion(FauxGestionnaire(jeton=self.jeton))[0], 200)
        self.assertIsNone(connecte(self.jeton))
        with transaction() as cx:
            self.assertEqual(cx.execute("SELECT count(*) AS n FROM comptes WHERE id = %s", (self.compte,)).fetchone()["n"], 0)
            self.assertEqual(cx.execute("SELECT count(*) AS n FROM noeuds WHERE id = 'mienne00000'").fetchone()["n"], 0)
            medias = {m["id"]: m["proprietaire_id"] for m in cx.execute("SELECT id, proprietaire_id FROM medias")}
        self.assertEqual(medias, {"partage00000": autre})
        self.assertFalse(existe("seul.mp4") or existe("seul00000000-mini.jpg") or existe("bob.mp4"))
        self.assertTrue(existe("partage.mp4"))
        self.assertEqual(self.signaux, [{autre}])
