import os
import tempfile
import unittest

from selixy_flux.resolution.cookies import avec_cookies


class TestCookies(unittest.TestCase):
    def setUp(self):
        dossier = tempfile.TemporaryDirectory()
        self.addCleanup(dossier.cleanup)
        self.source = os.path.join(dossier.name, 'source.txt')
        self.copie = os.path.join(dossier.name, 'copie.txt')

    def test_sans_fichier_les_options_sont_inchangees(self):
        self.assertEqual(avec_cookies({'a': 1}, self.source, self.copie), {'a': 1})

    def test_avec_fichier_une_copie_est_utilisee(self):
        with open(self.source, 'w', encoding='utf-8') as fichier:
            fichier.write('contenu')
        options = avec_cookies({'a': 1}, self.source, self.copie)
        self.assertEqual(options, {'a': 1, 'cookiefile': self.copie})
        with open(self.copie, encoding='utf-8') as fichier:
            self.assertEqual(fichier.read(), 'contenu')

    def test_la_copie_de_travail_est_gardee_tant_que_la_source_na_pas_change(self):
        with open(self.source, 'w', encoding='utf-8') as fichier:
            fichier.write('origine')
        avec_cookies({}, self.source, self.copie)
        with open(self.copie, 'w', encoding='utf-8') as fichier:
            fichier.write('renouvelee par yt-dlp')
        avec_cookies({}, self.source, self.copie)
        with open(self.copie, encoding='utf-8') as fichier:
            self.assertEqual(fichier.read(), 'renouvelee par yt-dlp')

    def test_une_source_plus_recente_remplace_la_copie(self):
        with open(self.source, 'w', encoding='utf-8') as fichier:
            fichier.write('nouvelle')
        with open(self.copie, 'w', encoding='utf-8') as fichier:
            fichier.write('ancienne')
        os.utime(self.copie, (1, 1))
        avec_cookies({}, self.source, self.copie)
        with open(self.copie, encoding='utf-8') as fichier:
            self.assertEqual(fichier.read(), 'nouvelle')
