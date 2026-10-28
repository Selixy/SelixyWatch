# bibliotheque

Façade de lecture de la bibliothèque en base, utilisée par les autres domaines (canaux, chat, flux) : `est_playlist`, `pistes` (ordre de
la playlist), `media` (forme publique, la même que l'ancien `medias.json` : `nom, genre, duree, t` + `source, yt` pour YouTube, ou
`ext, taille, mini` pour un fichier). Chaque fonction reçoit la connexion en paramètre.

## Vue du compte et outils des écritures

- `GET /api/bibliotheque` (`routes.py`, `vue.py`) : quatre requêtes en tout (nœuds visibles par requête récursive, pistes, médias, profils
  des propriétaires). Visibles : tout l'arbre du compte, plus les sous-arbres partagés avec lui (rôle le plus fort rencontré). `parent` vaut
  `"racine"` pour une racine de la vue du compte, l'identifiant du parent sinon (plus de dossier virtuel « partages »). Chaque nœud porte
  `partage_racine` : vrai si le compte n'en est pas propriétaire et que son parent réel ne lui est pas accessible (« Quitter » au lieu de supprimer).
  La vue d'un compte (`vue_compte.py`) : sa ligne `rangements` si elle existe (parent, nom, rang perso), sinon les valeurs réelles ; un parent
  invisible remonte le nœud à la racine. Sans compte : 401
  (renvoyé par la route, les GET ne passent pas par le gestionnaire d'erreurs).
- `connecte.py` : `exiger_connecte(h)` (401). `ecriture.py` : transaction prise sous le verrou global, pour toutes les écritures qui
  appellent les crochets de `canaux.synchro`. `champs.py` : validation des identifiants reçus en JSON (400 au lieu d'une erreur SQL).
  `visibilite.py` : un média est visible du compte s'il en est propriétaire ou s'il figure dans une playlist qu'il peut lire ;
  `concernes_media` donne les comptes à prévenir d'un changement sur un média.
- `lecture.py` est le contrat partagé avec les autres agents : il ne change pas.
