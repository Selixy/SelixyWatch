from selixy_watch.comptes.pseudo import canonique, squelette, valider
from selixy_watch.erreurs import Refus

AVATARS = {"png": "png", "jpg": "jpg", "jpeg": "jpg", "webp": "webp"}


def pseudos_finaux(profils, renommages):
    return {ident: renommages.get(p.get("pseudo", ""), p.get("pseudo", "")) for ident, p in profils.items()}


def valider_tous(finaux, proprietaire=""):
    valides, invalides = {}, []
    for ident, pseudo in finaux.items():
        try:
            propre = valider(pseudo, reserve_permis=canonique(pseudo) == canonique(proprietaire))
        except Refus as e:
            invalides.append((ident, pseudo, e.message))
            continue
        valides[ident] = {"pseudo": propre, "canonique": canonique(propre), "squelette": squelette(propre)}
    return valides, invalides


def collisions(valides):
    groupes = {}
    for ident, c in valides.items():
        groupes.setdefault(c["squelette"], []).append((ident, c["pseudo"]))
    return [g for g in groupes.values() if len(g) > 1]


def comptes_a_creer(profils, valides):
    comptes = []
    for ident, c in valides.items():
        p = profils[ident]
        avatar = AVATARS.get(str(p.get("avatar") or "").lower())
        comptes.append({"id": ident, **c, "avatar": avatar, "version": int(p.get("v") or 0) if avatar else 0})
    return comptes
