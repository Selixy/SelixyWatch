import time

from selixy_flux.journal import journal
from selixy_flux.relais.erreurs import ErreurAmont, ErreurBlocage


class Frein:
    def __init__(self, duree, horloge=time.monotonic):
        self.duree = duree
        self.horloge = horloge
        self.jusqua = 0

    def moderer(self, resoudre):
        def moderee(yt):
            if self.horloge() < self.jusqua:
                raise ErreurAmont(429)
            try:
                return resoudre(yt)
            except ErreurBlocage:
                self.jusqua = self.horloge() + self.duree
                journal.warning('YouTube bloque la résolution : aucune requête pendant %s s', self.duree)
                raise
        return moderee
