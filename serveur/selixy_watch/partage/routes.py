from selixy_watch.partage.routes_gestion import lire, quitter, retirer, revoquer
from selixy_watch.partage.routes_invitation import accepter_invitation, inviter, voir

ROUTES_GET = {"/api/partage": lire}

ROUTES_POST = [
    (r"/api/invitations", inviter),
    (r"/api/partage/([^/]+)/retirer", retirer),
    (r"/api/partage/([^/]+)/revoquer", revoquer),
    (r"/api/partage/([^/]+)/quitter", quitter),
    (r"/api/invitation/voir", voir),
    (r"/api/invitation/accepter", accepter_invitation),
]
