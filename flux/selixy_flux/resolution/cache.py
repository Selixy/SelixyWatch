import threading
import time


class CacheTemporaire:
    def __init__(self, duree, horloge=time.monotonic):
        self.duree = duree
        self.horloge = horloge
        self.entrees = {}
        self.verrou = threading.Lock()

    def obtenir(self, cle, fabrique):
        with self.verrou:
            trouve = self.entrees.get(cle)
            if trouve and trouve[0] > self.horloge():
                return trouve[1]
            valeur = fabrique(cle)
            self.entrees[cle] = (self.horloge() + self.duree, valeur)
            return valeur

    def oublier(self, cle):
        with self.verrou:
            self.entrees.pop(cle, None)
