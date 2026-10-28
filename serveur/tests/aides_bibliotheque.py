import json
import os
import unittest
from unittest.mock import patch

from tests.aides_bdd import ADRESSE, compte, connexion_vierge
from tests.aides_http import FauxGestionnaire
from tests.aides_synchro import installer_synchro

if ADRESSE:
    os.environ["BDD_URL"] = ADRESSE

from selixy_watch.bdd.connexion import fermer, transaction
from selixy_watch.bdd.migrations import migrer
from selixy_watch.erreurs import Refus


def publics_factices(cx, ids):
    return {i: {"id": i, "pseudo": f"pseudo-{i}", "avatar": None} for i in ids}


class CasBibliotheque(unittest.TestCase):
    def setUp(self):
        connexion = connexion_vierge()
        migrer(connexion)
        for ident in ("a", "b", "c"):
            compte(connexion, ident, f"Nom{ident}", f"nom{ident}", f"nom{ident}")
        connexion.commit()
        connexion.close()
        fermer()
        self.synchro = installer_synchro()
        for cible, effet in (("comptes.session.ident", lambda h: h.ident), ("comptes.profils.publics", publics_factices)):
            demarre = patch(f"selixy_watch.{cible}", create=True, side_effect=effet)
            demarre.start()
            self.addCleanup(demarre.stop)
        for nom in ("avant_retrait", "playlist_modifiee", "playlist_supprimee"):
            demarre = patch.object(self.synchro, nom)
            setattr(self, nom, demarre.start())
            self.addCleanup(demarre.stop)
        self.addCleanup(fermer)

    def appeler(self, ident, route, *groupes, corps=None):
        octets = json.dumps(corps).encode() if corps is not None else b""
        return route(FauxGestionnaire(ident, octets), *groupes)

    def refus(self, ident, route, *groupes, corps=None):
        with self.assertRaises(Refus) as contexte:
            self.appeler(ident, route, *groupes, corps=corps)
        return contexte.exception.code

    def partager(self, nid, ident, role):
        with transaction() as cx:
            cx.execute("INSERT INTO partages (noeud_id, compte_id, role) VALUES (%s, %s, %s)", (nid, ident, role))
