import time

from selixy_watch.acces import droits
from selixy_watch.bibliotheque import lecture
from selixy_watch.bibliotheque.ecriture import ecriture
from selixy_watch.canaux import synchro
from selixy_watch.diffusion.bibliotheque import signaler
from selixy_watch.playlist.ajout_youtube import ajouter_youtube

LOT_MAX = 5
DELAI_MAX = 1


class SuiviImport:
    def __init__(self, playlist, compte):
        self.playlist = playlist
        self.compte = compte
        self.ajoutes = 0
        self.en_attente = 0
        self.dernier = time.time()

    def ajouter(self, yt, nom, duree):
        if ajouter_youtube(self.playlist, self.compte, yt, nom, duree):
            self.ajoutes += 1
            self.en_attente += 1
        if self.en_attente and (self.en_attente >= LOT_MAX or time.time() - self.dernier >= DELAI_MAX):
            self.publier()

    def publier(self):
        with ecriture() as cx:
            existe = lecture.est_playlist(cx, self.playlist)
            concernes = droits.concernes(cx, self.playlist) if existe else set()
            if existe:
                synchro.playlist_modifiee(cx, self.playlist)
        signaler(concernes)
        self.en_attente, self.dernier = 0, time.time()
