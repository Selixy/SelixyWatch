# flux

Service de lecture de flux YouTube, prévu pour tourner en conteneur à côté de l'API et de nginx (même `127.0.0.1`).
Il n'est pas branché sur le site pour l'instant (voir plus bas).

## Routes

- `GET /flux/sante` : santé.
- `GET /flux/<id média>/info` : durée et types MIME (avec codecs) des deux pistes, en JSON.
- `GET /flux/<id média>/video` et `/audio` : la piste, relayée avec `Range`.

L'identifiant de média (12 caractères hexadécimaux) fait office d'autorisation : seul un média `source: youtube` de
`donnees/medias.json` (lu en lecture seule) est servi, jamais une adresse fournie par le client.

## Organisation

- `flux.py` : point d'entrée. `selixy_flux/entrees/` : serveur HTTP et routes. `resolution/` : yt-dlp, cache des adresses, lecture de
  `medias.json`. `relais/` : plage, requête amont, service (réessai).
- `tests/` : `python3 -m unittest discover -s tests -t .` depuis `flux/`. Aucun accès réseau.
- `Containerfile` : image Debian slim avec `yt-dlp[default]` (mise à jour à chaque construction ; l'extra `default` apporte `yt-dlp-ejs`, sans
  lequel le défi « n » de YouTube échoue : « The page needs to be reloaded ») et deno (yt-dlp refuse les anciennes versions : 2.1.4
  était rejetée, 2.9.7 acceptée).

## Pièges et arbitrages

- YouTube ne publie plus de format combiné image + son (constaté sur `yt-dlp -F`, même avec un runtime JavaScript récent) : le service
  sélectionne une piste vidéo H.264 (720p au plus) et une piste audio AAC, en MP4 fragmenté. Le navigateur les assemble (voir
  `ui/js/lecteur/flux/`), le serveur ne fait aucun transcodage.
- Le relais borne chaque requête amont à 10 Mo : googlevideo bride les lectures sans borne. Le navigateur redemande la suite.
- Les adresses résolues sont gardées 30 min, liées à l'IP du VPS, d'où le relais plutôt qu'une redirection. Si l'amont répond une erreur
  (adresse expirée), l'adresse est résolue de nouveau une fois.
- Frein : dès qu'une résolution échoue sur « Sign in to confirm you're not a bot », plus aucune requête vers YouTube pendant 10 min
  (réponse 502 immédiate). Sans lui, chaque échec faisait sauter le lecteur à la vidéo suivante : une résolution par seconde sur toute la
  playlist, ce qui aggrave le signalement. Le lecteur met désormais la room en pause au lieu de sauter.
- La résolution est sérialisée par un verrou (une seule extraction yt-dlp à la fois, 256 Mo de mémoire).
- Piste vidéo à plus de 10 Mo par segment : non gérée (le relais couperait le segment). Non rencontré à 720p.

## Cookies YouTube

YouTube refuse la résolution depuis l'adresse IP d'un serveur (« Sign in to confirm you're not a bot »). Si `/secrets/cookies.txt` existe,
yt-dlp l'utilise (copié dans `/tmp` : le montage est en lecture seule et yt-dlp réécrit son fichier). La copie est gardée tant que
l'original n'est pas plus récent, pour conserver les cookies que YouTube renouvelle pendant une résolution. Le fichier est au format
Netscape, exporté d'un compte secondaire, et ne doit jamais entrer dans le dépôt. Les cookies expirent : il faut les ré-exporter.

## Conteneur

- `Containerfile` : image Python avec yt-dlp et deno, lancée sous un utilisateur sans droits.
- Derrière nginx, `location /flux/` doit pointer vers `127.0.0.1:8082`.
