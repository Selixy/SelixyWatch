import os

import psycopg
from psycopg.rows import dict_row

ADRESSE = os.environ.get("BDD_URL_TEST")
RAISON = "BDD_URL_TEST absent : lancer outils/banc-bdd.sh demarrer"


def connexion_vierge():
    connexion = psycopg.connect(ADRESSE, autocommit=False, row_factory=dict_row)
    connexion.execute("DROP SCHEMA public CASCADE")
    connexion.execute("CREATE SCHEMA public")
    connexion.commit()
    return connexion


def compte(connexion, ident, pseudo, canonique, squelette):
    connexion.execute(
        "INSERT INTO comptes (id, pseudo, pseudo_canonique, pseudo_squelette) VALUES (%s, %s, %s, %s)",
        (ident, pseudo, canonique, squelette),
    )
