import os
import re

from selixy_watch.bdd.connexion import transaction
from selixy_watch.comptes.courriel_compte import definir_email
from selixy_watch.comptes.confirmation import confirmer
from selixy_watch.comptes.inscription import inscription
from selixy_watch.courriel import envoi
from tests.aides_comptes import appeler, jeton_de_reponse, preparer_base

MDP = "motdepasse1"


def preparer_courriel():
    os.environ["MAIL_URL"] = "memoire"
    preparer_base()
    envoi.BOITE_MEMOIRE.clear()


def inscrire(pseudo):
    return jeton_de_reponse(appeler(inscription, {"pseudo": pseudo, "mdp": MDP}))


def jeton_du_dernier_mail():
    return re.search(r"#(\S+)", envoi.BOITE_MEMOIRE[-1]["texte"]).group(1)


def valider_email(session, adresse):
    appeler(definir_email, {"email": adresse, "mdp": MDP}, jeton=session)
    return appeler(confirmer, {"jeton": jeton_du_dernier_mail()})


def ligne_compte(pseudo):
    with transaction() as cx:
        return cx.execute("SELECT * FROM comptes WHERE pseudo = %s", (pseudo,)).fetchone()
