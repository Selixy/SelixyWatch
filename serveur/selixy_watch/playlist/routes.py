from selixy_watch.bibliotheque.connecte import exiger_connecte
from selixy_watch.entrees.echange import corps_json
from selixy_watch.playlist.actions import action_playlist


def route_playlist(h, pid, action):
    ident = exiger_connecte(h)
    return 200, action_playlist(ident, pid, action, corps_json(h))


ROUTES_POST = [(r"/api/playlist/([0-9a-f]{12})/(ajouter|retirer|deplacer)", route_playlist)]
