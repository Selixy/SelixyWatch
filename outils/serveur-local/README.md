# serveur-local

Fait tourner tout le site sur ta machine pour vérifier un résultat : `python3 outils/serveur-local/demarrer.py`, puis
`http://127.0.0.1:8080/`. Il lance l'API (`serveur/watch.py`, port 3240, cookie non sécurisé car pas de HTTPS en local) et sert `ui/`
comme le ferait nginx en production : `/api/` relayé vers l'API, `/medias/` et `/avatars/` lus dans le
dossier de données. Arrêt : Ctrl+C (l'API s'arrête avec lui).

Base de données : l'API a besoin de PostgreSQL. Sans `BDD_URL`, `demarrer.py` lance un PostgreSQL jetable avec `outils/banc-bdd.sh demarrer` (podman, port 55432, données perdues à l'arrêt) et l'arrête avec Ctrl+C ; avec `BDD_URL=postgresql://…`, il utilise cette base et n'y touche pas. Le Python qui lance le script doit avoir `psycopg[binary,pool]` (`serveur/requirements.txt`).

Variables : `PORT_LOCAL` (8080), `PORT_API` (3240), `LATENCE_MEDIAS` (secondes d'attente avant chaque envoi de média, 0 par défaut : pour voir la room attendre son média), `DONNEES_LOCALES` (par défaut `watch-local` dans le dossier temporaire du système).

`python3 outils/serveur-local/demarrer.py --donnees-test` crée au premier démarrage une playlist « Test (vidéo factice) » avec une vidéo de
2 minutes (compteur et bip, fabriquée par `ffmpeg`, environ 19 Mo) et sa miniature, pour pouvoir essayer la room. Un fichier
`donnees-test-semees` dans le dossier de données évite de la recréer. Pour l'ajouter à un serveur déjà lancé :
`python3 outils/serveur-local/donnees_test.py 3240`.

- `demarrer.py` : lance l'API et le serveur.
- `passerelle.py` : le gestionnaire HTTP (fichiers de `ui/`, relais vers l'API, flux SSE compris).
- `donnees_test.py` : la vidéo factice et son envoi par l'API (`ffmpeg` requis).
- `medias.py` : envoi d'un fichier avec les requêtes Range. Sans elles, on ne peut pas se placer dans une vidéo.

## Limites

- Pas de service `flux/` (le flux vidéo du pod) : ce qui en dépend ne marche pas en local.
- Les en-têtes de cache sont désactivés (`no-cache`), donc un rechargement montre toujours la dernière version des fichiers.
- Pas de HTTPS : la caméra, le micro et le partage d'écran des navigateurs fonctionnent sur `127.0.0.1`, mais pas depuis un autre appareil
  du réseau.
