import io
import json
import sys
import types
import unittest
from unittest import mock

from selixy_watch.bdd import connexion
from selixy_watch.bdd.migrations import migrer
from selixy_watch.comptes import profils, session
from selixy_watch.erreurs import Refus
from tests.aides_bdd import compte, connexion_vierge

try:
    from selixy_watch.diffusion import bibliotheque
except ImportError:
    bibliotheque = types.ModuleType("selixy_watch.diffusion.bibliotheque")
    bibliotheque.signaler = lambda comptes: None
    sys.modules["selixy_watch.diffusion.bibliotheque"] = bibliotheque
    import selixy_watch.diffusion as diffusion

    diffusion.bibliotheque = bibliotheque


def faux_gestionnaire(ident, corps):
    donnees = json.dumps(corps).encode()
    entetes = {"Content-Length": str(len(donnees))}
    return types.SimpleNamespace(compte=ident, headers=entetes, rfile=io.BytesIO(donnees))


class BancPartage(unittest.TestCase):
    def setUp(self):
        base = connexion_vierge()
        migrer(base)
        for ident in ("a", "b", "c"):
            compte(base, ident, ident.upper(), ident, ident)
        noeuds = [
            ("dossier000001", "a", None, "dossier"),
            ("playlist00001", "a", "dossier000001", "playlist"),
            ("playlist00002", "a", None, "playlist"),
            ("playlistdeb01", "b", None, "playlist"),
        ]
        for ident, proprietaire, parent, type_ in noeuds:
            base.execute(
                "INSERT INTO noeuds (id, proprietaire_id, parent_id, type, nom) VALUES (%s, %s, %s, %s, %s)",
                (ident, proprietaire, parent, type_, ident),
            )
        base.commit()
        base.close()
        self.signaux = []
        for cible, nom, valeur in (
            (session, "ident", lambda h: h.compte),
            (profils, "publics", lambda cx, ids: {i: {"id": i, "pseudo": f"pseudo_{i}", "avatar": None} for i in ids}),
            (bibliotheque, "signaler", lambda comptes: self.signaux.append(set(comptes))),
        ):
            patch = mock.patch.object(cible, nom, valeur, create=True)
            patch.start()
            self.addCleanup(patch.stop)

    def tearDown(self):
        connexion.fermer()

    def appeler(self, route, ident, corps, *groupes):
        try:
            return route(faux_gestionnaire(ident, corps), *groupes)
        except Refus as r:
            return r.code, {"erreur": r.message}

    def requete(self, sql, params=()):
        with connexion.transaction() as cx:
            return cx.execute(sql, params).fetchall()
