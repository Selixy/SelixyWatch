import json
import unittest

from selixy_flux.entrees.routes import repondre
from tests.aides import refuser
from tests.aides_routes import lire_factice, services

MEDIA = '/flux/aaaaaaaaaaaa'


class TestRoutes(unittest.TestCase):
    def test_sante(self):
        statut, _, corps = repondre('/flux/sante', None, services())
        self.assertEqual((statut, b''.join(corps)), (200, b'{"ok": 1}'))

    def test_media_inconnu_ou_chemin_invalide(self):
        for chemin in ('/flux/bbbbbbbbbbbb/video', '/flux/../etc', MEDIA, MEDIA + '/texte', MEDIA + '/video/x', '/autre'):
            self.assertEqual(repondre(chemin, None, services())[0], 404)

    def test_informations(self):
        statut, entetes, corps = repondre(MEDIA + '/info', None, services())
        self.assertEqual((statut, json.loads(b''.join(corps)), entetes['Content-Length']), (200, {'duree': 5}, '12'))

    def test_relaie_piste_statut_entetes_et_octets(self):
        appels = []
        statut, entetes, corps = repondre(MEDIA + '/audio', 'bytes=0-3', services(lire_factice(appels)))
        self.assertEqual((statut, entetes['Content-Range'], b''.join(corps)), (206, 'bytes 0-3/9', b'abcd'))
        self.assertEqual(appels, [('dQw4w9WgXcQ', 'audio', 'bytes=0-3')])

    def test_amont_en_echec_donne_502(self):
        self.assertEqual(repondre(MEDIA + '/video', None, services(refuser))[0], 502)
