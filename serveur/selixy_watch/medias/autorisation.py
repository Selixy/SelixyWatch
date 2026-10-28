from selixy_watch.erreurs import Refus


def exiger_envoi(cx, compte):
    ligne = cx.execute("SELECT offre, admin, email_valide_le FROM comptes WHERE id = %s", (compte,)).fetchone()
    if ligne is None or (ligne["offre"] != "pro" and not ligne["admin"]):
        raise Refus(402, "L'envoi de fichiers est réservé aux comptes Pro.")
    if ligne["email_valide_le"] is None:
        raise Refus(403, "Validez votre adresse e-mail pour envoyer des fichiers.")
