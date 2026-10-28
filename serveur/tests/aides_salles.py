import io
import json
from unittest.mock import patch

from selixy_watch.bdd.connexion import fermer
from selixy_watch.bdd.migrations import migrer
from selixy_watch.etat import ABONNES, CANAUX, DERNIER_MESSAGE, ETATS_VOCAL
from tests.aides_bdd import compte, connexion_vierge

MODULES_ECRITURE = ("canaux.actions", "canaux.synchro", "canaux.occupation", "canaux.rattrapage")


class FauxGestionnaire:
    def __init__(self, qui, corps):
        donnees = json.dumps(corps).encode()
        self.headers = {"qui": qui, "Content-Length": str(len(donnees))}
        self.rfile = io.BytesIO(donnees)


def faux_h(qui, corps=None):
    return FauxGestionnaire(qui, corps or {})


def public_simule(ident):
    return {"id": ident, "pseudo": ident.capitalize(), "avatar": None}


def preparer(cas):
    ABONNES.clear()
    CANAUX.clear()
    DERNIER_MESSAGE.clear()
    ETATS_VOCAL.clear()
    for nom in MODULES_ECRITURE:
        cas.enterContext(patch(f"selixy_watch.{nom}.ecrire_json"))
    cas.enterContext(patch("selixy_watch.canaux.acces_salle.ident", lambda h: h.headers["qui"]))
    cas.enterContext(patch("selixy_watch.chat.messages.public", public_simule))
    cas.enterContext(patch("selixy_watch.vocal.signal.public", public_simule))
    cas.enterContext(patch("selixy_watch.comptes.profils.publics", lambda cx, ids: {i: public_simule(i) for i in ids}, create=True))
    cas.addCleanup(fermer)


def monde():
    cx = connexion_vierge()
    migrer(cx)
    for ident in ("alice", "bob", "carl"):
        compte(cx, ident, ident.capitalize(), ident, ident)
    cx.execute("INSERT INTO noeuds (id, proprietaire_id, type, nom) VALUES ('pl1', 'alice', 'playlist', 'P1')")
    for rang, mid in enumerate(("m1", "m2")):
        cx.execute("INSERT INTO medias (id, proprietaire_id, source, nom, genre, duree, fichier) VALUES (%s, 'alice', 'fichier', %s, 'audio', 100, %s)", (mid, mid, mid + ".mp3"))
        cx.execute("INSERT INTO playlist_medias (playlist_id, media_id, rang) VALUES ('pl1', %s, %s)", (mid, rang))
    cx.execute("INSERT INTO partages (noeud_id, compte_id, role) VALUES ('pl1', 'bob', 'lecteur')")
    cx.commit()
    return cx
