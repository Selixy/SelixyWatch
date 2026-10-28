from selixy_watch.arbre import rangement
from selixy_watch.bibliotheque.champs import identifiant
from selixy_watch.bibliotheque.vue_compte import charger
from selixy_watch.erreurs import Refus
from selixy_watch.texte import propre


def renommer(cx, ident, d):
    nid = identifiant(d.get("id"), "nom ou élément invalide")
    nom = propre(d.get("nom", ""), 120)
    if not nom:
        raise Refus(400, "nom ou élément invalide")
    vue = charger(cx, ident)
    if nid not in vue:
        raise Refus(404, "élément inconnu")
    rangement.nommer(cx, ident, vue[nid], nom)
    return {"ok": 1}, {ident}
