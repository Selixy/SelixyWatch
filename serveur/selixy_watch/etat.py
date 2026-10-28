import threading

from selixy_watch.persistance import lire_json

CANAUX = lire_json("canaux.json", {})
DERNIER_MESSAGE = {}
DERNIERE_REACTION = {}
ABONNES = {}
ETATS_VOCAL = {}
UNITES = {"jour": "", "n": 0}
CACHE_YT = {}
verrou = threading.RLock()
verrou_unites = threading.Lock()
imports = threading.BoundedSemaphore(2)
recherches = threading.BoundedSemaphore(4)
