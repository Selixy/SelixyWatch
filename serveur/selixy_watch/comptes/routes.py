from selixy_watch.comptes.anonyme import anonyme
from selixy_watch.comptes.avatar import avatar, supprimer_avatar
from selixy_watch.comptes.confirmation import confirmer
from selixy_watch.comptes.courriel_compte import definir_email, supprimer_email
from selixy_watch.comptes.inscription import connexion, inscription
from selixy_watch.comptes.recuperation import changer, demander
from selixy_watch.comptes.moi import changer_mdp, moi, renommer
from selixy_watch.comptes.sessions_gestion import deconnexion, deconnexion_partout, lister, revoquer
from selixy_watch.comptes.suppression import supprimer

ROUTES_GET = {
    "/api/moi": moi,
    "/api/moi/sessions": lister,
}

ROUTES_POST = [
    (r"/api/inscription", inscription),
    (r"/api/anonyme", anonyme),
    (r"/api/connexion", connexion),
    (r"/api/moi", renommer),
    (r"/api/moi/mdp", changer_mdp),
    (r"/api/moi/avatar", avatar),
    (r"/api/moi/avatar/supprimer", supprimer_avatar),
    (r"/api/moi/sessions/revoquer", revoquer),
    (r"/api/moi/supprimer", supprimer),
    (r"/api/moi/email", definir_email),
    (r"/api/moi/email/supprimer", supprimer_email),
    (r"/api/email/confirmer", confirmer),
    (r"/api/recuperation", demander),
    (r"/api/recuperation/mdp", changer),
    (r"/api/deconnexion", deconnexion),
    (r"/api/deconnexion/partout", deconnexion_partout),
]
