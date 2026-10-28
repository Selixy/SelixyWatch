from tests.aides_partage import BancPartage

from selixy_watch.partage.routes_invitation import accepter_invitation, inviter

DOSSIER = "dossier000001"


def creer_invitation(banc, noeuds=(DOSSIER,), usages=5):
    return banc.appeler(inviter, "a", {"noeuds": list(noeuds), "usages_max": usages})[1]


class BancAvecInvite(BancPartage):
    def setUp(self):
        super().setUp()
        self.invitation = creer_invitation(self)
        self.appeler(accepter_invitation, "b", {"jeton": self.invitation["jeton"]})
        self.signaux.clear()
