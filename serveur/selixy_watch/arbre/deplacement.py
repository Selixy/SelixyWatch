from selixy_watch.arbre import rangement, vue_perso
from selixy_watch.bibliotheque.champs import identifiant, identifiant_facultatif
from selixy_watch.bibliotheque.vue_compte import charger
from selixy_watch.configuration import RACINE
from selixy_watch.erreurs import Refus


def parent_voulu(vue, vers):
    if vers == RACINE:
        return None
    if vers not in vue or vue[vers]["type"] != "dossier":
        raise Refus(400, "déplacement invalide")
    return vers


def deplacer(cx, ident, d):
    nid = identifiant(d.get("id"), "déplacement invalide")
    vers = identifiant(d.get("vers", RACINE), "déplacement invalide")
    avant = identifiant_facultatif(d.get("avant"))
    vue = charger(cx, ident)
    if nid not in vue:
        raise Refus(404, "élément inconnu")
    parent = parent_voulu(vue, vers)
    vue_perso.verifier(vue, nid, parent)
    ordre = rangement.ordre_apres(vue, nid, parent, avant)
    for rang, id_ in enumerate(ordre):
        if id_ == nid or vue[id_]["rang"] != rang:
            rangement.ecrire(cx, ident, vue, vue[id_], parent, rang)
    return {"ok": 1}, {ident}
