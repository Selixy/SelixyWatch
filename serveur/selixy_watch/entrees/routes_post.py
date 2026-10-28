import re

from selixy_watch.arbre.routes import ROUTES_POST as ROUTES_ARBRE
from selixy_watch.canaux.route import ROUTES_POST as ROUTES_CANAUX
from selixy_watch.chat.messages import ROUTES_POST as ROUTES_CHAT
from selixy_watch.comptes.routes import ROUTES_POST as ROUTES_COMPTES
from selixy_watch.liens.route import ROUTES_POST as ROUTES_LIENS
from selixy_watch.medias.miniature import ROUTES_POST as ROUTES_MINIATURE
from selixy_watch.medias.reception import ROUTES_POST as ROUTES_MEDIAS
from selixy_watch.partage.routes import ROUTES_POST as ROUTES_PARTAGE
from selixy_watch.playlist.routes import ROUTES_POST as ROUTES_PLAYLIST
from selixy_watch.vocal.signal import ROUTES_POST as ROUTES_VOCAL

ROUTES_POST = [
    (re.compile(motif), traitement)
    for motif, traitement in (
        ROUTES_MEDIAS + ROUTES_LIENS + ROUTES_COMPTES + ROUTES_ARBRE + ROUTES_PLAYLIST
        + ROUTES_MINIATURE + ROUTES_CHAT + ROUTES_VOCAL + ROUTES_CANAUX + ROUTES_PARTAGE
    )
]
