import os

DOSSIER = os.environ.get("STATE_DIRECTORY", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "donnees"))
DOSSIER_MEDIAS = os.path.join(DOSSIER, "medias")
DOSSIER_AVATARS = os.path.join(DOSSIER, "avatars")
BDD_HOTE = os.environ.get("BDD_HOTE", "127.0.0.1")
BDD_PORT = int(os.environ.get("BDD_PORT", "5432"))
BDD_NOM = os.environ.get("BDD_NOM", "selixy_watch")
BDD_UTILISATEUR = os.environ.get("BDD_UTILISATEUR", "selixy_watch")
BDD_MDP_FICHIER = os.environ.get("BDD_MDP_FICHIER", "/secrets/bdd_mdp.txt")
PORT = int(os.environ.get("PORT", "3240"))
HOTE = os.environ.get("HOTE", "127.0.0.1")
MAX_MEDIA = int(os.environ.get("MAX_MEDIA_MO", "4096")) * 1024 * 1024
COOKIE_SECURE = os.environ.get("COOKIE_SECURE", "1") == "1"
MAX_NOEUDS = 3000
MAX_PROFONDEUR = 8
MAX_CHAT = 100
MAX_TEXTE = 500
MAX_AVATAR = 64 * 1024
MAX_MINIATURE = 200 * 1024
MAX_LIEN = 200
MAX_YT_PLAYLIST = 100
MAX_YT_API = 200
MAX_UNITES = 9000
RACINE = "racine"
EMOJIS = ("❤️", "😂", "😮", "👏", "🔥", "🎉")
ENTETES_WEB = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0",
    "Accept-Language": "fr,en",
    "Cookie": "SOCS=CAI; CONSENT=YES+1",
}
