import json
import os
import tempfile
import unittest

from selixy_flux.resolution.medias import identifiant_youtube


class TestMedias(unittest.TestCase):
    def setUp(self):
        self.dossier = tempfile.TemporaryDirectory()
        self.addCleanup(self.dossier.cleanup)
        self.chemin = os.path.join(self.dossier.name, 'medias.json')
        medias = {
            'aaaaaaaaaaaa': {'source': 'youtube', 'yt': 'dQw4w9WgXcQ'},
            'bbbbbbbbbbbb': {'ext': 'mp4'},
            'cccccccccccc': {'source': 'youtube', 'yt': '../../etc'},
        }
        with open(self.chemin, 'w', encoding='utf-8') as fichier:
            json.dump(medias, fichier)

    def test_media_youtube_connu(self):
        self.assertEqual(identifiant_youtube(self.chemin, 'aaaaaaaaaaaa'), 'dQw4w9WgXcQ')

    def test_fichier_et_inconnu_refuses(self):
        self.assertIsNone(identifiant_youtube(self.chemin, 'bbbbbbbbbbbb'))
        self.assertIsNone(identifiant_youtube(self.chemin, 'zzzzzzzzzzzz'))
        self.assertIsNone(identifiant_youtube(self.chemin + '.absent', 'aaaaaaaaaaaa'))

    def test_identifiant_malforme_refuse(self):
        self.assertIsNone(identifiant_youtube(self.chemin, 'cccccccccccc'))
