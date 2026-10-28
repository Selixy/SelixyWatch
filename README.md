# SelixyWatch

Un site pour regarder des vidéos et écouter de la musique à plusieurs, chacun chez soi, à la même seconde. Il y a des playlists qu'on
partage, des rooms avec un chat et un vocal, un lecteur YouTube intégré et des comptes.

En ligne sur [watch.selixy.dev](https://watch.selixy.dev). La fiche du projet est sur [selixy.dev/selixy-watch](https://selixy.dev/selixy-watch/).
Le projet est en cours depuis octobre 2026 : certaines parties sont solides, d'autres sont encore à l'essai (voir plus bas).

## Ce que ça fait

- **Playlists** : des dossiers imbriqués, un rangement par glisser-déposer, un même média dans plusieurs playlists. On y met des fichiers,
  des résultats de recherche YouTube, ou on colle un lien YouTube ou Spotify (pour Spotify, le serveur retrouve chaque morceau sur YouTube
  en prenant la durée la plus proche).
- **Rooms** : tous ceux qui sont dans la room voient et entendent la même chose. File « À suivre » avec boucle et aléatoire partagés,
  chat, réactions emoji, mode cinéma, raccourcis clavier. Le son reste local à chacun.
- **Vocal et vidéo** : en WebRTC. Le serveur ne relaie que les messages d'établissement de la connexion.
- **Comptes** : pseudo et mot de passe, ou compte « Invité » éphémère. Partage d'un dossier ou d'une playlist par lien d'invitation,
  confirmation d'adresse e-mail et récupération de compte par courriel, quotas d'envoi de fichiers.

## Comment la synchro marche

Le serveur garde l'état de chaque room (média, position, lecture ou pause) et le diffuse en SSE. Chaque navigateur mesure son écart avec
l'horloge du serveur (`/api/heure`), calcule la position où il devrait être, et corrige dès que la dérive dépasse 0,4 s, vérifiée chaque
seconde. La position affichée vient toujours de l'état du serveur, jamais du lecteur local. Les commandes (lecture, pause, saut) repartent
par de simples requêtes POST : j'ai pris SSE plutôt que des WebSockets parce que le flux ne va que dans un sens.

## La difficulté : la même seconde, et ce que YouTube refuse

Tenir tout le monde sur la même seconde, c'est surtout gérer les écarts : latence, démarrage lent d'un lecteur, pub qui retarde quelqu'un,
onglet en arrière-plan, navigateur qui bloque le son tant qu'on n'a pas cliqué.

Avec YouTube, le lecteur vit dans un cadre d'un autre site, donc le site ne peut ni retirer les pubs ni masquer les étiquettes que YouTube
affiche après chaque saut. Il peut seulement remettre à la bonne seconde quelqu'un qui vient de subir une pub.

J'avais essayé de ne plus dépendre du lecteur de YouTube : le dossier `flux/` contient un petit service qui résout les pistes avec yt-dlp
et les relaie, pour que le navigateur les assemble. Techniquement ça marche, mais YouTube refuse les requêtes qui viennent de l'adresse d'un
serveur, même avec des cookies. Le lecteur est donc revenu à l'iframe, et ce service n'est pas branché sur le site.

## Pile technique

- `ui/` : site statique, modules JavaScript écrits à la main, sans compilation ni bibliothèque. Une « coque » garde les trois vues (room,
  playlists, profil) chargées chacune dans son cadre, pour que la lecture continue quand on change de page.
- `serveur/` : API en Python (bibliothèque standard + `psycopg`), PostgreSQL, migrations SQL numérotées. Seul l'état de lecture des rooms
  est gardé en mémoire, parce qu'il change chaque seconde et se reconstruit au redémarrage. Mots de passe hachés en scrypt.
- `flux/` : le service de flux décrit plus haut (Python, yt-dlp), non branché.
- `outils/` : un serveur local pour essayer le site, un PostgreSQL jetable pour les tests, et un script d'audit des règles de code.
- `tests/ui/` et `serveur/tests/`, `flux/tests/` : les tests.

## Règles de code

Je me suis imposé : 200 lignes et cinq fonctions au plus par fichier, une responsabilité par fichier, pas de commentaire dans le code
(le pourquoi va dans le `README.md` du module). `outils/audit-modulaire.sh` mesure tout ça. Le code des premières versions, écrit avant
ces règles, est listé dans `outils/audit-exceptions.txt`. Les READMEs des modules sont en français.

## Lancer en local

Il faut Python 3, Node, et soit Podman (pour un PostgreSQL jetable) soit une base PostgreSQL à vous (`BDD_URL`).

    python3 -m venv .venv && .venv/bin/pip install -r serveur/requirements.txt
    .venv/bin/python outils/serveur-local/demarrer.py

Puis ouvrir `http://127.0.0.1:8080/`. Le détail est dans `outils/serveur-local/README.md`. Les réglages que le code lit sont listés dans
`secrets.modele` (noms seulement). Sans clé YouTube, la recherche passe par la page de résultats, qui peut être bloquée.

## Tests

    node --test tests/ui/*.test.js
    (cd flux && python3 -m unittest discover -s tests -t .)
    outils/banc-bdd.sh demarrer          # affiche une adresse, à mettre dans BDD_URL_TEST
    (cd serveur && BDD_URL_TEST=<adresse> ../.venv/bin/python -m unittest discover -s tests -t .)
    outils/audit-modulaire.sh

## Où j'en suis

La synchro, les playlists, les comptes, le partage et le chat fonctionnent. Le vocal et la vidéo sont récents et peu éprouvés, je n'ai
pas de recul sur leur tenue à plus de quelques personnes. La lecture YouTube dépend de ce que YouTube tolère. Il reste du code hérité à
remettre aux règles. Ce dépôt est une version nettoyée pour la vitrine : la configuration de déploiement du site en ligne n'y est pas.

## Licence

MIT, voir `LICENSE`. La police « SelixyWatch Sans » dérive de Roboto (SIL Open Font License 1.1, texte dans `ui/polices/OFL.txt`).
