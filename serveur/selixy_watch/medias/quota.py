from selixy_watch.erreurs import Refus


def utilise(cx, compte):
    return int(cx.execute("SELECT COALESCE(sum(taille), 0) AS total FROM medias WHERE proprietaire_id = %s", (compte,)).fetchone()["total"])


def exiger_place(cx, compte, octets):
    ligne = cx.execute("SELECT quota_octets, admin FROM comptes WHERE id = %s", (compte,)).fetchone()
    if ligne is None:
        raise Refus(507, "Quota d'espace atteint.")
    if not ligne["admin"] and utilise(cx, compte) + octets > ligne["quota_octets"]:
        raise Refus(507, "Quota d'espace atteint.")
