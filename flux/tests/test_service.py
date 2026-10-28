import json
import unittest

from selixy_flux.relais.erreurs import ErreurAmont
from selixy_flux.relais.service import informations, lire
from selixy_flux.resolution.cache import CacheTemporaire
from tests.aides import Resolveur, accepter, refuser, refuser_premiere_adresse


class TestService(unittest.TestCase):
    def setUp(self):
        self.resoudre = Resolveur()
        self.cache = CacheTemporaire(100)

    def test_une_seule_resolution_pour_deux_pistes(self):
        self.assertEqual(lire('v', 'video', None, self.cache, self.resoudre, accepter)[2], 'video1')
        self.assertEqual(lire('v', 'audio', None, self.cache, self.resoudre, accepter)[2], 'audio1')
        self.assertEqual(len(self.resoudre.appels), 1)

    def test_adresse_expiree_est_resolue_de_nouveau(self):
        resultat = lire('v', 'video', None, self.cache, self.resoudre, refuser_premiere_adresse)
        self.assertEqual(resultat[2], 'video2')

    def test_deuxieme_echec_remonte(self):
        with self.assertRaises(ErreurAmont):
            lire('v', 'video', None, self.cache, self.resoudre, refuser)
        self.assertEqual(len(self.resoudre.appels), 2)

    def test_informations_en_json(self):
        self.assertEqual(json.loads(informations('v', self.cache, self.resoudre)), {'duree': 5})
