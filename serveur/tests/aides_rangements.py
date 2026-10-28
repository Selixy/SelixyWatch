from selixy_watch.arbre.routes import route_arbre
from selixy_watch.bibliotheque.routes import route_bibliotheque
from selixy_watch.partage.routes_invitation import accepter_invitation, inviter
from tests.aides_arbre import creer_noeud
from tests.aides_bibliotheque import CasBibliotheque


class CasRangements(CasBibliotheque):
    def vue(self, ident):
        code, corps = self.appeler(ident, route_bibliotheque, None)
        self.assertEqual(code, 200)
        return {n["id"]: n for n in corps["noeuds"]}

    def deplacer(self, ident, nid, vers, avant=None):
        return self.appeler(ident, route_arbre, "deplacer", corps={"id": nid, "vers": vers, "avant": avant})

    def renommer(self, ident, nid, nom):
        return self.appeler(ident, route_arbre, "renommer", corps={"id": nid, "nom": nom})

    def inviter_et_accepter(self, proprietaire, invite, noeuds):
        _, lien = self.appeler(proprietaire, inviter, corps={"noeuds": list(noeuds)})
        return self.appeler(invite, accepter_invitation, corps={"jeton": lien["jeton"]})

    def arbre_partage(self):
        haut = creer_noeud(self, "a", "Haut")
        bas = creer_noeud(self, "a", "Bas", parent=haut)
        liste = creer_noeud(self, "a", "Liste", "playlist", bas)
        return haut, bas, liste
