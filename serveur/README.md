# serveur

API de SelixyWatch : bibliothèque standard Python et `psycopg` (PostgreSQL), dans l'image `Containerfile` (`requirements.txt`). Point d'entrée :
`python watch.py` (le conteneur lance exactement `python /app/watch.py`). Le code vit dans le paquet `selixy_watch/`, découpé par domaine ;
`watch.py` ne fait qu'appeler `demarrer_serveur()`.

## Principe

Chaque compte a sa bibliothèque : des dossiers imbriqués qui rangent des playlists, qui contiennent des médias (fichiers envoyés ou vidéos
YouTube). Un dossier ou une playlist se partage par lien d'invitation (lecteur ou éditeur), le partage vaut pour tout le sous-arbre. Chaque
playlist est aussi une « room » : tous ceux qui y ont accès et l'écoutent voient et entendent la même seconde. Comptes : pseudo + mot de passe,
ou anonyme éphémère (supprimé, avec tout ce qui n'est lié qu'à lui, à la déconnexion). Sans compte, on ne voit rien.

La base PostgreSQL est la source de vérité (comptes, sessions, arbres, médias, partages, invitations, chat). Seul l'état de lecture des rooms
reste en mémoire (`canaux.json`), parce qu'il change chaque seconde et se reconstruit au redémarrage.

## Modules

- `configuration.py` : constantes et variables d'environnement. `etat.py` : état partagé en mémoire (canaux, abonnés SSE, verrous).
  `persistance.py` : écriture JSON (`canaux.json`, export `medias.json`). `demarrage.py` : migrations, export, horloge, entretien, serveur HTTP.
- `bdd/` : connexion, migrations SQL, import des anciennes données JSON (`import_json/`, `importer_json.py`).
- `entrees/` : HTTP. `gestionnaire.py` (`do_GET`/`do_POST` : aiguillage par motif, `Refus` → code et `{"erreur"}`), `routes_get.py` et
  `routes_post.py` (tables assemblées depuis les `ROUTES_GET`/`ROUTES_POST` de chaque domaine), `echange.py` (réponse JSON, corps de requête).
- Domaines : `comptes/` (inscription, sessions, mots de passe, frein, anonymes, purge), `acces/` (droits sur un nœud), `bibliotheque/` (lecture,
  vue d'un compte, export pour le service flux), `arbre/`, `playlist/`, `medias/`, `partage/` (invitations), `canaux/` (état de lecture, synchro
  avec la bibliothèque), `chat/`, `vocal/`, `flux/` (SSE), `diffusion/` (événements, présence, signal `bibliotheque`), `liens/`, `youtube/`, `spotify/`.
  Chaque domaine a son README.
- Ajouter une route = ajouter une entrée dans le `ROUTES_*` de son domaine. Ajouter une commande de canal = une fonction dans `canaux/` et une
  ligne dans `COMMANDES`. Ajouter une source d'import = une fonction dans `liens/importation.py` et une ligne dans `SOURCES`. Changer le schéma
  = un nouveau fichier `bdd/migrations/NNN_nom.sql`, jamais la modification d'un ancien.
- Les fonctions de route reçoivent le gestionnaire HTTP (`h`) puis les groupes de l'URL, et renvoient `(code, corps[, en-têtes])`. Les routes
  GET reçoivent `(h, url)`. Le flux SSE répond lui-même et renvoie `None`.
- Une commande de canal renvoie `True` (version incrémentée), `False` (état modifié sans changer la version) ou `None` (rien à faire).

## Routes

- `GET /api/heure` : `{"t": secondes}`. `GET /api/sante` : `{"ok": 1, "cle_youtube": bool}`.
- Comptes (détail dans `comptes/README.md`) : `POST /api/inscription`, `/api/connexion`, `/api/anonyme`, `GET|POST /api/moi`, `POST /api/moi/mdp`,
  `/api/moi/avatar`, `/api/moi/avatar/supprimer`, `GET /api/moi/sessions`, `POST /api/moi/sessions/revoquer`, `/api/moi/supprimer`,
  `/api/deconnexion`, `/api/deconnexion/partout`. Cookie `session` (jeton aléatoire ; seul son sha256 est en base).
- `GET /api/bibliotheque` : la vue du compte (`noeuds` avec `role` et `proprietaire`, `medias`) ; racines `parent: "racine"` (à soi) ou
  `"partages"` (reçues).
- `GET /api/flux[?canal=<playlist>]` (SSE) : `canaux`, `canal`, `presence`, `chat`, `reaction`, `signal`, `import`, `bibliotheque` (relire la vue).
- `POST /api/medias` : corps = fichier brut ; en-têtes `X-Nom` (encodé URL), `X-Duree`, `X-Playlist` (obligatoire, rôle éditeur). Le type vient des
  premiers octets, pas du nom. Quota par compte. `POST /api/medias/<id>/miniature` (jpeg, 200 Ko, propriétaire du média).
- `POST /api/arbre/<creer|renommer|deplacer|supprimer>`, `POST /api/playlist/<id>/<ajouter|retirer|deplacer>` (rôle éditeur).
- `POST /api/liens {"url","playlist"}` : répond 202, import en arrière-plan (200 morceaux au plus par lien, 2 imports à la fois, sinon 429).
- Partage (détail dans `partage/README.md`) : `POST /api/partage/<id>/<inviter|retirer|role|revoquer|quitter>`, `GET /api/partage?noeud=<id>`,
  `POST /api/invitation/voir`, `POST /api/invitation/accepter`.
- `POST /api/canal/<id>/<lire|pause|aller|jouer|suivant|precedent|fin|boucle|aleatoire>`, `/message {"texte"}` (500 caractères, un message
  toutes les 0,7 s), `/reaction {"emoji"}` (six emojis), `/signal` (vocal/vidéo) : rôle lecteur au moins.
- `GET /api/recherche?q=` : au plus 12 vidéos YouTube.
- Fichiers : `$STATE_DIRECTORY` (sinon `serveur/donnees`) : `canaux.json`, `medias.json` (export des références YouTube pour le service flux,
  réécrit à chaque changement de la bibliothèque), `medias/`, `avatars/` ; écriture atomique (fichier temporaire puis `os.replace`).

## Pièges et décisions

- L'état en mémoire est protégé par un seul verrou réentrant (`etat.verrou`) ; aucun appel réseau sous verrou (la base est locale). Les diffusions SSE se font sous verrou.
- Les structures de `etat.py` sont modifiées en place, jamais réaffectées : les modules les importent par nom.
- Le service flux lit `medias.json` (lecture seule, sans accès à la base) pour savoir quelles vidéos YouTube il peut servir : l'API le réexporte
  depuis la base au démarrage et à chaque `diffusion.bibliotheque.signaler`.
- Le frein de connexion et le cache de session par requête sont en mémoire et locaux au processus : à revoir si l'API tourne un jour en plusieurs
  processus (frein en base ou dans un cache partagé).
- Purge d'un compte : la base d'abord (une transaction), les fichiers ensuite (`comptes.purge.achever`), pour ne jamais laisser une ligne
  sans son fichier si la transaction échoue. Les anonymes éphémères sans session valide sont purgés au démarrage puis toutes les 10 minutes.
- État d'un canal : `{courant, lecture, pos, t0, v, boucle, aleatoire, suite, t}`. `pos` = position (s) à l'instant `t0` (heure serveur) si lecture,
  sinon position figée ; `melange` = ordre aléatoire courant, tenu seulement quand `aleatoire` est actif et jamais envoyé aux clients. `suite` = les
  pistes qui suivent le courant dans l'ordre actif, en bouclant. En fin de liste on repart au début (nouveau mélange en aléatoire, sans rejouer de suite le même média).
- `v` : version de la lecture. `fin` est signalé par chaque spectateur ; seul le premier compte, car média et version doivent correspondre à
  l'état courant. `boucle` et `aleatoire` ne changent pas `v` pour ne pas invalider les `fin` en route. `suivant` ignore la boucle.
- `canaux/rattrapage.py` : toutes les secondes, les canaux dont le média est fini depuis plus d'une seconde (`TOLERANCE_FIN`) avancent même sans
  spectateur (onglet fermé, son bloqué). Au plus 200 pistes par passage (`PASSES_MAX`). Le suivant est daté de la fin du précédent, pas de maintenant.
- `canaux/occupation.py` : quand un utilisateur rejoint un canal inoccupé (aucun abonné actif dans `ABONNES`), la lecture démarre automatiquement si la playlist contient des médias. Si le canal est déjà occupé, son état n'est pas perturbé et le nouvel arrivant s'aligne localement sur l'état en cours. Quand le dernier abonné quitte le canal, la lecture se met automatiquement en pause à la position courante pour éviter que le temps ne défile dans le vide.
- Retirer le média en cours d'une playlist passe au suivant (ou arrête) avant de retirer la piste.
- Fichiers écrits en 0644 : lisibles par le conteneur nginx qui les sert.
- Une vidéo YouTube n'existe qu'une fois dans la bibliothèque, même dans plusieurs playlists ; sans fichier, le navigateur la lit avec le
  lecteur YouTube intégré. Un import ajoute les pistes par lots de 5 ou toutes les secondes (`liens/suivi.py`) pour que la playlist se remplisse à vue.
- Clé YouTube officielle (facultative) : `$STATE_DIRECTORY/cle_youtube.txt`, relue à chaque appel (pas de redémarrage), ou `YOUTUBE_API_KEY`. Elle donne
  titres, durées, playlists (200 vidéos) et recherches sans passer par les pages, que YouTube bloque parfois depuis un serveur (« êtes-vous un
  robot »). Sans clé, ou si l'API échoue, on lit les pages (100 vidéos pour une playlist). La clé n'apparaît jamais dans un message d'erreur.
- Quota (`youtube/quota.py`) : 9000 unités par jour au plus (le quota gratuit est de 10 000), compteur local par jour UTC ; une recherche coûte 100
  unités, le reste 1.
- La recherche lit d'abord la page de résultats (gratuit) ; si elle est bloquée ou vide, l'API officielle prend le relais. Les titres vus alimentent
  `CACHE_YT` (une heure) : ajouter un résultat retrouve titre et durée sans relire la page de la vidéo, souvent bloquée alors que la recherche passe.
- Les en-têtes web (`ENTETES_WEB`) portent un cookie `SOCS`/`CONSENT` pour éviter la page de consentement européenne de YouTube.
- Un morceau Spotify est retrouvé sur YouTube : parmi les 5 premiers résultats, la durée la plus proche, à 10 s près sinon le premier.
- Les noms de playlist (60 caractères) et de média (120) passent par `texte.propre` : caractères imprimables, espaces compactés.
- `X-Duree` : bornée à 0–86400 s, 0 si illisible.
- Tests (banc local) : comparer les réponses JSON de toutes les routes avant/après un changement, hors horodatages et identifiants tirés au hasard.
