from selixy_flux.relais.erreurs import ErreurAmont
from selixy_flux.resolution.source import Lecture


class Resolveur:
    def __init__(self):
        self.appels = []

    def __call__(self, yt):
        self.appels.append(yt)
        n = len(self.appels)
        return Lecture(f'video{n}', f'audio{n}', {'duree': 5})


def accepter(source, plage):
    return 206, {}, source


def refuser(*arguments):
    raise ErreurAmont(403)


def refuser_premiere_adresse(source, plage):
    return refuser() if source == 'video1' else accepter(source, plage)
