import secrets

from selixy_watch.comptes.frein import bloque, echec
from selixy_watch.comptes.inscription import entetes_session
from selixy_watch.comptes.ouverture import ouvrir
from selixy_watch.comptes.profils import forme
from selixy_watch.comptes.pseudo import canonique, squelette
from selixy_watch.comptes.pseudo_libre import ecrire_sans_doublon
from selixy_watch.comptes.requete import adresse_client, agent_client
from selixy_watch.erreurs import Refus

FENETRE = 3600
CREATIONS_MAX = 20
ESSAIS = 20


def creer_invite(h):
    pseudo = f"Invité-{secrets.randbelow(10000):04d}"
    identifiant = secrets.token_hex(8)

    def ecrire(cx):
        ligne = cx.execute(
            "INSERT INTO comptes (id, pseudo, pseudo_canonique, pseudo_squelette, ephemere) VALUES (%s, %s, %s, %s, true) "
            "RETURNING id, pseudo, avatar, avatar_version",
            (identifiant, pseudo, canonique(pseudo), squelette(pseudo)),
        ).fetchone()
        return forme(ligne), ouvrir(cx, identifiant, agent_client(h))

    return ecrire_sans_doublon(pseudo, ecrire)


def anonyme(h):
    cle = ("anonyme", adresse_client(h))
    if bloque([cle], FENETRE, CREATIONS_MAX):
        raise Refus(429, "Trop de comptes invités créés depuis cette adresse. Réessayez plus tard.")
    for _ in range(ESSAIS):
        try:
            public, jeton = creer_invite(h)
        except Refus as refus:
            if refus.code != 409:
                raise
            continue
        echec([cle], FENETRE)
        return 201, {**public, "ephemere": True}, entetes_session(jeton)
    raise Refus(503, "Impossible de créer un compte invité pour le moment.")
