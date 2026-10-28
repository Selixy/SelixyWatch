from selixy_watch.bdd.connexion import transaction
from selixy_watch.medias.reception import recevoir_media
from tests.aides_http import FauxGestionnaire

MP3 = b"ID3\x03\x00\x00\x00\x00\x00\x00" + b"\x00" * 64


def envoyer(ident, playlist, contenu=MP3):
    entetes = {"X-Playlist": playlist, "X-Nom": "Chanson.mp3", "X-Duree": "12.5"}
    return recevoir_media(FauxGestionnaire(ident, contenu, entetes))


def definir_quota(ident, octets):
    with transaction() as cx:
        cx.execute(
            "UPDATE comptes SET offre = 'pro', email = %s, email_valide_le = now(), quota_octets = %s WHERE id = %s",
            (f"{ident}@exemple.fr", octets, ident),
        )


def regler_offre(ident, offre, valide, quota):
    with transaction() as cx:
        cx.execute(
            "UPDATE comptes SET offre = %s, email_valide_le = CASE WHEN %s THEN now() END, quota_octets = %s WHERE id = %s",
            (offre, valide, quota, ident),
        )
