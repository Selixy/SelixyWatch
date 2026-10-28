import unittest

from selixy_watch.bdd.import_json.principal import executer
from tests.aides_bdd import connexion_vierge
from tests.aides_import_json import fabrique_transaction, jeu_json


class BancImport(unittest.TestCase):
    def setUp(self):
        self.connexion = connexion_vierge()
        self.dossier = jeu_json()

    def tearDown(self):
        self.connexion.close()

    def lignes(self, sql):
        return self.connexion.execute(sql).fetchall()

    def lancer(self, *options):
        return executer(["--dossier", self.dossier, "--proprietaire", "Marion_", *options], fabrique_transaction(self.connexion))
