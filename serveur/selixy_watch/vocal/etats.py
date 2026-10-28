from selixy_watch.diffusion.evenements import diffuser_canal
from selixy_watch.etat import ABONNES, ETATS_VOCAL


def etats_du_canal(canal):
    return {k[1]: v for k, v in ETATS_VOCAL.items() if k[0] == canal}


def signal_initial(canal):
    return ("signal", {"canal": canal, "action": "init_etats", "etats": etats_du_canal(canal)})


def quitter_vocal(canal, ident):
    if any(info.get("canal") == canal and info.get("ident") == ident for info in ABONNES.values()):
        return
    if (canal, ident) in ETATS_VOCAL:
        ETATS_VOCAL.pop((canal, ident), None)
        diffuser_canal(canal, "signal", {"canal": canal, "de": ident, "action": "depart"})
