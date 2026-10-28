import unittest

from selixy_flux.relais.amont import ouvrir
from selixy_flux.relais.erreurs import ErreurAmont
from selixy_flux.resolution.source import Source
from tests.faux_amont import CONTENU, demarrer_faux_amont


class TestAmont(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.serveur = demarrer_faux_amont()
        cls.base = f'http://127.0.0.1:{cls.serveur.server_port}'

    @classmethod
    def tearDownClass(cls):
        cls.serveur.shutdown()

    def test_plage_relayee_avec_entetes(self):
        statut, entetes, flux = ouvrir(Source(self.base + '/v', {}), 'bytes=10-19')
        self.assertEqual((statut, entetes['Content-Range'], flux.read()), (206, 'bytes 10-19/100', CONTENU[10:20]))

    def test_plage_hors_limites_transmise_en_416(self):
        statut, entetes, _ = ouvrir(Source(self.base + '/v', {}), 'bytes=500-600')
        self.assertEqual((statut, entetes['Content-Range']), (416, 'bytes */100'))

    def test_refus_amont_leve_une_erreur(self):
        with self.assertRaises(ErreurAmont):
            ouvrir(Source(self.base + '/interdit', {}), 'bytes=0-1')
