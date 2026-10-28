import urllib.error
import urllib.request

from selixy_flux.relais.erreurs import ErreurAmont

ENTETES_RELAYES = ('Content-Type', 'Content-Length', 'Content-Range', 'Accept-Ranges')


def ouvrir(source, plage):
    requete = urllib.request.Request(source.url, headers={**source.entetes, 'Range': plage})
    try:
        reponse = urllib.request.urlopen(requete, timeout=20)
    except urllib.error.HTTPError as erreur:
        if erreur.code != 416:
            raise ErreurAmont(erreur.code) from erreur
        reponse = erreur
    except (urllib.error.URLError, TimeoutError) as erreur:
        raise ErreurAmont(0) from erreur
    entetes = {nom: reponse.headers[nom] for nom in ENTETES_RELAYES if reponse.headers.get(nom)}
    return reponse.status, entetes, reponse
