from selixy_watch.erreurs import Refus


def identifiant(valeur, message="identifiant invalide"):
    if not isinstance(valeur, str) or not valeur:
        raise Refus(400, message)
    return valeur


def identifiant_facultatif(valeur, message="position invalide"):
    if valeur is not None and not isinstance(valeur, str):
        raise Refus(400, message)
    return valeur
