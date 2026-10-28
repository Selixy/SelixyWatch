import re

from selixy_flux.journal import journal
from selixy_flux.relais.erreurs import ErreurAmont

MOTIF_MEDIA = re.compile(r'/flux/([0-9a-f]{12})/(info|video|audio)')
JSON = {'Content-Type': 'application/json'}


def reponse_json(statut, texte):
    corps = texte if isinstance(texte, bytes) else texte.encode('utf-8')
    return statut, {**JSON, 'Content-Length': str(len(corps))}, iter([corps])


def servir(services, yt, piste, plage):
    if piste == 'info':
        return reponse_json(200, services.informations(yt))
    statut, entetes, flux = services.lire(yt, piste, plage)
    return statut, entetes, iter(lambda: flux.read(65536), b'')


def repondre(chemin, plage, services):
    if chemin == '/flux/sante':
        return reponse_json(200, '{"ok": 1}')
    trouve = MOTIF_MEDIA.fullmatch(chemin)
    yt = services.identifiant(trouve.group(1)) if trouve else None
    if yt is None:
        return reponse_json(404, '{"erreur": "inconnu"}')
    try:
        return servir(services, yt, trouve.group(2), plage)
    except ErreurAmont as erreur:
        journal.error('flux %s de %s indisponible (amont %s)', trouve.group(2), yt, erreur.statut)
        return reponse_json(502, '{"erreur": "flux indisponible"}')
