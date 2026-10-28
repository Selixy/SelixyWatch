from selixy_watch.bdd.connexion import transaction
from selixy_watch.canaux.acces_salle import compte_autorise
from selixy_watch.comptes.profils import public
from selixy_watch.diffusion.evenements import diffuser_canal
from selixy_watch.entrees.echange import corps_json
from selixy_watch.etat import ETATS_VOCAL, verrou


def signal(h, cid):
    d = corps_json(h, 65536)
    with verrou, transaction() as cx:
        i = compte_autorise(cx, h, cid)
        act, donnee, cible = d.get("action"), d.get("data"), d.get("cible")
        if act == "etat" and isinstance(donnee, dict):
            ETATS_VOCAL[(cid, i)] = {"micro": bool(donnee.get("micro")), "camera": bool(donnee.get("camera"))}
        elif act == "depart":
            ETATS_VOCAL.pop((cid, i), None)
        diffuser_canal(cid, "signal", {
            "canal": cid,
            "de": i,
            "pseudo": public(i)["pseudo"],
            "cible": cible,
            "action": act,
            "data": donnee,
        })
    return 200, {"ok": 1}


ROUTES_POST = [(r"/api/canal/([0-9a-f]{12})/signal", signal)]
