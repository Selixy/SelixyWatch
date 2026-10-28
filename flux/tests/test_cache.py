import unittest

from selixy_flux.resolution.cache import CacheTemporaire


class TestCache(unittest.TestCase):
    def setUp(self):
        self.heure = [0]
        self.appels = []
        self.cache = CacheTemporaire(100, lambda: self.heure[0])

    def fabrique(self, cle):
        self.appels.append(cle)
        return len(self.appels)

    def test_reutilise_avant_expiration(self):
        self.cache.obtenir('a', self.fabrique)
        self.heure[0] = 99
        self.assertEqual(self.cache.obtenir('a', self.fabrique), 1)

    def test_recalcule_apres_expiration(self):
        self.cache.obtenir('a', self.fabrique)
        self.heure[0] = 101
        self.assertEqual(self.cache.obtenir('a', self.fabrique), 2)

    def test_oublier_force_le_recalcul(self):
        self.cache.obtenir('a', self.fabrique)
        self.cache.oublier('a')
        self.assertEqual(self.cache.obtenir('a', self.fabrique), 2)
