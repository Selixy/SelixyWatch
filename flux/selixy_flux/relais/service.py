import json

from selixy_flux.relais.erreurs import ErreurAmont
from selixy_flux.relais.plage import plage_amont

PISTES = ('video', 'audio')


def lire(yt, piste, entete_plage, cache, resoudre, ouvrir):
    plage = plage_amont(entete_plage)
    try:
        return ouvrir(getattr(cache.obtenir(yt, resoudre), piste), plage)
    except ErreurAmont:
        cache.oublier(yt)
    return ouvrir(getattr(cache.obtenir(yt, resoudre), piste), plage)


def informations(yt, cache, resoudre):
    return json.dumps(cache.obtenir(yt, resoudre).informations).encode('utf-8')
