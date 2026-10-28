from selixy_watch.erreurs import Refus


def chaine(corps, cle):
    valeur = corps.get(cle)
    if not isinstance(valeur, str) or not valeur:
        raise Refus(400, f"Champ {cle} manquant.")
    return valeur


def entier_borne(corps, cle, defaut, minimum, maximum):
    nombre = corps.get(cle, defaut)
    if isinstance(nombre, bool) or not isinstance(nombre, int) or not minimum <= nombre <= maximum:
        raise Refus(400, f"{cle} : valeur attendue entre {minimum} et {maximum}.")
    return nombre


def liste_noeuds(corps):
    noeuds = corps.get("noeuds")
    if not isinstance(noeuds, list) or not 1 <= len(noeuds) <= 50:
        raise Refus(400, "noeuds : entre 1 et 50 éléments attendus.")
    if any(not isinstance(n, str) or not n for n in noeuds) or len(set(noeuds)) != len(noeuds):
        raise Refus(400, "noeuds : identifiants valides et sans doublon attendus.")
    return noeuds
