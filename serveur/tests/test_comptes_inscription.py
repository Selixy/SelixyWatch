import threading
import unittest

from selixy_watch.bdd.connexion import transaction
from selixy_watch.comptes.inscription import inscription
from selixy_watch.comptes.session import hacher_jeton
from tests.aides_bdd import ADRESSE, RAISON
from tests.aides_comptes import appeler, jeton_de_reponse, preparer_base


@unittest.skipUnless(ADRESSE, RAISON)
class TestInscription(unittest.TestCase):
    def setUp(self):
        preparer_base()

    def test_inscription_reussie(self):
        code, public, entetes = appeler(inscription, {"pseudo": "Intel", "mdp": "motdepasse1"})
        self.assertEqual(code, 201)
        self.assertEqual(public["pseudo"], "Intel")
        jeton = jeton_de_reponse((code, public, entetes))
        with transaction() as cx:
            compte = cx.execute("SELECT mdp_hash FROM comptes WHERE id = %s", (public["id"],)).fetchone()
            session = cx.execute("SELECT compte_id FROM sessions WHERE jeton_hash = %s", (hacher_jeton(jeton),)).fetchone()
            clair = cx.execute("SELECT count(*) AS n FROM sessions WHERE jeton_hash = %s", (jeton,)).fetchone()
        self.assertTrue(compte["mdp_hash"].startswith("scrypt$16384$8$1$"))
        self.assertEqual(session["compte_id"], public["id"])
        self.assertEqual(clair["n"], 0)
        self.assertTrue(any("mu=" in v and "Max-Age=0" in v for _, v in entetes))

    def test_mot_de_passe_invalide(self):
        self.assertEqual(appeler(inscription, {"pseudo": "Intel", "mdp": "court"})[0], 400)
        self.assertEqual(appeler(inscription, {"pseudo": "Intel", "mdp": "x" * 129})[0], 400)

    def test_course_deux_inscriptions(self):
        barriere = threading.Barrier(2)
        codes = []

        def tenter(mdp):
            barriere.wait()
            codes.append(appeler(inscription, {"pseudo": "Course", "mdp": mdp})[0])

        fils = [threading.Thread(target=tenter, args=(f"motdepasse{n}",)) for n in range(2)]
        [f.start() for f in fils]
        [f.join() for f in fils]
        self.assertEqual(sorted(codes), [201, 409])
        with transaction() as cx:
            self.assertEqual(cx.execute("SELECT count(*) AS n FROM comptes").fetchone()["n"], 1)
