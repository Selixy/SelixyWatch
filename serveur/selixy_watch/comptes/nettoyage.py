from selixy_watch.bdd.connexion import transaction
from selixy_watch.comptes.purge import achever, purger_compte

EXPIRES = (
    "SELECT id FROM comptes WHERE ephemere AND NOT EXISTS "
    "(SELECT 1 FROM sessions s WHERE s.compte_id = comptes.id AND s.expire_le > now())"
)


def purger_ephemeres_expires(cx):
    return [purger_compte(cx, ligne["id"]) for ligne in cx.execute(EXPIRES).fetchall()]


def nettoyer():
    with transaction() as cx:
        purges = purger_ephemeres_expires(cx)
    achever(purges)
