from selixy_watch.administration.commandes import trouver


def definir_admin(cx, pseudo, valeur):
    compte = trouver(cx, pseudo)
    cx.execute("UPDATE comptes SET admin = %s WHERE id = %s", (valeur, compte["id"]))
    return f"{compte['pseudo']} : {'administrateur' if valeur else 'plus administrateur'}."
