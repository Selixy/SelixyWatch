import os
import stat
import tempfile
import unittest

from selixy_watch.configuration import DOSSIER
from selixy_watch.persistance import ecrire_json


def mode_de(nom):
    return stat.S_IMODE(os.stat(os.path.join(DOSSIER, nom)).st_mode)


class TestPersistance(unittest.TestCase):
    def test_donnees_privees_par_defaut(self):
        ecrire_json("profils.json", {})
        self.assertEqual(mode_de("profils.json"), 0o600)

    def test_medias_lisibles_par_le_service_flux(self):
        ecrire_json("medias.json", {}, 0o644)
        self.assertEqual(mode_de("medias.json"), 0o644)
