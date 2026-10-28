class Echec:
    def __init__(self, erreur):
        self.erreur = erreur
        self.appels = []

    def __call__(self, yt):
        self.appels.append(yt)
        raise self.erreur
