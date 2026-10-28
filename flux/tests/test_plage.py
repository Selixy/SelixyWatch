import unittest

from selixy_flux.relais.plage import TAILLE_BLOC, plage_amont


class TestPlage(unittest.TestCase):
    def test_absente_commence_au_debut(self):
        self.assertEqual(plage_amont(None), f'bytes=0-{TAILLE_BLOC - 1}')

    def test_ouverte_est_bornee_a_un_bloc(self):
        self.assertEqual(plage_amont('bytes=1000-'), f'bytes=1000-{1000 + TAILLE_BLOC - 1}')

    def test_fermee_courte_est_conservee(self):
        self.assertEqual(plage_amont('bytes=10-99'), 'bytes=10-99')

    def test_fermee_trop_longue_est_bornee(self):
        self.assertEqual(plage_amont('bytes=0-999999999'), f'bytes=0-{TAILLE_BLOC - 1}')

    def test_illisible_commence_au_debut(self):
        self.assertEqual(plage_amont('bytes=-500'), f'bytes=0-{TAILLE_BLOC - 1}')
