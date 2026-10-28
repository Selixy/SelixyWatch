import io
import json
import os

from selixy_watch.bdd.connexion import fermer
from selixy_watch.bdd.migrations import migrer
from selixy_watch.comptes import frein
from selixy_watch.comptes.session import ident
from tests.aides_bdd import ADRESSE, connexion_vierge


class FauxGestionnaire:
    def __init__(self, corps=None, jeton=None, ip="10.0.0.1", brut=None, cookie_brut=None):
        donnees = brut if brut is not None else json.dumps(corps or {}).encode()
        cookie = cookie_brut if cookie_brut is not None else (f"session={jeton}" if jeton else "")
        self.headers = {"Content-Length": str(len(donnees)), "Cookie": cookie, "X-Real-IP": ip, "User-Agent": "banc"}
        self.rfile = io.BytesIO(donnees)
        self.client_address = ("127.0.0.1", 1)


def preparer_base():
    os.environ["BDD_URL"] = ADRESSE
    fermer()
    connexion = connexion_vierge()
    migrer(connexion)
    connexion.commit()
    connexion.close()
    frein.reinitialiser()


def jeton_de_reponse(reponse):
    for nom, valeur in reponse[2]:
        if valeur.startswith("session="):
            return valeur.split(";")[0].split("=", 1)[1]
    return None


def appeler(route, corps=None, jeton=None, ip="10.0.0.1"):
    try:
        return route(FauxGestionnaire(corps, jeton, ip))
    except Exception as erreur:
        if hasattr(erreur, "code"):
            return erreur.code, {"erreur": erreur.message}, []
        raise


def connecte(jeton):
    return ident(FauxGestionnaire(jeton=jeton))

