import unittest

from selixy_flux.relais.erreurs import ErreurAmont, ErreurBlocage
from selixy_flux.resolution.frein import Frein
from tests.aides_frein import Echec


class TestFrein(unittest.TestCase):
    def setUp(self):
        self.heure = [0]
        self.frein = Frein(600, lambda: self.heure[0])

    def test_apres_un_blocage_plus_aucune_requete(self):
        echec = Echec(ErreurBlocage(0))
        moderee = self.frein.moderer(echec)
        with self.assertRaises(ErreurBlocage):
            moderee('a')
        with self.assertRaises(ErreurAmont):
            moderee('b')
        self.assertEqual(echec.appels, ['a'])

    def test_reprise_apres_la_duree(self):
        echec = Echec(ErreurBlocage(0))
        moderee = self.frein.moderer(echec)
        with self.assertRaises(ErreurBlocage):
            moderee('a')
        self.heure[0] = 601
        with self.assertRaises(ErreurBlocage):
            moderee('b')
        self.assertEqual(echec.appels, ['a', 'b'])

    def test_une_autre_erreur_ne_freine_pas(self):
        echec = Echec(ErreurAmont(0))
        moderee = self.frein.moderer(echec)
        for yt in ('a', 'b'):
            with self.assertRaises(ErreurAmont):
                moderee(yt)
        self.assertEqual(echec.appels, ['a', 'b'])
