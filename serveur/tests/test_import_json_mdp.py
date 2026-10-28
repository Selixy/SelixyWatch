import unittest

from selixy_watch.bdd.import_json.principal import executer
from selixy_watch.comptes.mdp import verifier
from tests.aides_banc_import import BancImport
from tests.aides_bdd import ADRESSE, RAISON
from tests.aides_import_json import fabrique_transaction


@unittest.skipUnless(ADRESSE, RAISON)
class TestImportJsonMdp(BancImport):
    def test_mot_de_passe_du_proprietaire_defini_a_l_import(self):
        code, _ = executer(["--dossier", self.dossier, "--proprietaire", "Marion_", "--renommer", "lntel=Lintel", "--appliquer", "--definir-mdp"],
                           fabrique_transaction(self.connexion), saisir_mdp=lambda: "secret-solide-42")
        self.assertEqual(code, 0)
        ligne = self.lignes("SELECT mdp_hash FROM comptes WHERE pseudo = 'Marion_'")[0]
        self.assertTrue(verifier("secret-solide-42", ligne["mdp_hash"]))
