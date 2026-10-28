import unicodedata

from selixy_watch.erreurs import Refus

LONGUEUR_MIN = 3
LONGUEUR_MAX = 24
SEPARATEURS = "_-."
RESERVES = ("admin", "administrateur", "root", "selixy", "selixywatch", "support", "moderateur", "modo", "systeme", "anonyme", "invite", "staff")
HOMOGLYPHES = str.maketrans({
    "а": "a", "е": "e", "о": "o", "р": "p", "с": "c", "у": "y", "х": "x", "і": "l", "ј": "j", "ѕ": "s", "ԁ": "d", "ӏ": "l",
    "α": "a", "ο": "o", "ι": "l", "κ": "k", "ν": "v", "ρ": "p", "τ": "t", "υ": "u", "ε": "e", "ɡ": "g",
    "0": "o", "1": "l", "i": "l", "3": "e", "5": "s", "$": "s", "@": "a",
})


def canonique(pseudo):
    return unicodedata.normalize("NFKC", pseudo).strip().casefold()


def squelette(pseudo):
    decompose = unicodedata.normalize("NFKD", canonique(pseudo))
    visible = "".join(c for c in decompose if not unicodedata.combining(c) and c not in SEPARATEURS and unicodedata.category(c)[0] != "C")
    return visible.translate(HOMOGLYPHES).replace("rn", "m").replace("vv", "w")


def ecriture(caractere):
    return unicodedata.name(caractere, "INCONNU").split()[0]


def valider(pseudo, reserve_permis=False):
    propre = unicodedata.normalize("NFKC", pseudo or "").strip()
    if not LONGUEUR_MIN <= len(propre) <= LONGUEUR_MAX:
        raise Refus(400, f"Le pseudo doit faire de {LONGUEUR_MIN} à {LONGUEUR_MAX} caractères.")
    if not all(c.isalnum() or c in SEPARATEURS for c in propre) or not propre[0].isalnum():
        raise Refus(400, "Le pseudo n'accepte que des lettres, des chiffres et _ - . (et commence par une lettre ou un chiffre).")
    if len({ecriture(c) for c in propre if c.isalpha()}) > 1:
        raise Refus(400, "Le pseudo ne peut pas mélanger plusieurs alphabets.")
    if not reserve_permis and any(squelette(propre) == squelette(r) for r in RESERVES):
        raise Refus(400, "Ce pseudo est réservé.")
    return propre
