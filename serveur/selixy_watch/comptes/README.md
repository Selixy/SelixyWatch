# comptes

Inscription, connexion, sessions, profil, avatar et suppression de compte, sur PostgreSQL.

## Décisions

- **Mots de passe** (`mdp.py`) : scrypt de `hashlib` (n=2^14, r=8, p=1, sel de 16 octets), stocké sous la forme `scrypt$n$r$p$sel$hash` (base64). Les
  paramètres sont dans l'empreinte, ce qui permet de les durcir plus tard sans casser les comptes existants. Comparaison par `hmac.compare_digest`.
  Quand le pseudo n'existe pas, une vérification contre une empreinte leurre est faite quand même, pour que le temps de réponse ne révèle pas
  l'existence du compte.
- **Sessions** (`session.py`, `ouverture.py`, `sessions_gestion.py`) : jeton `secrets.token_urlsafe(32)` dans le cookie `session`, seul son sha256 est en
  base. Durée de 30 jours, prolongée à l'usage s'il en reste moins de 15 (une seule requête `UPDATE ... RETURNING`). Quand la session est prolongée,
  `GET /api/moi` renvoie le cookie rafraîchi, sinon le navigateur l'oublierait au bout de 30 jours. L'ancien cookie `mu` n'est plus reconnu et est
  effacé à l'inscription et à la connexion.
- **`ident(h)`** met son résultat en cache sur le gestionnaire (`h.ident_session`). Le serveur répond en HTTP/1.0 : un gestionnaire sert une seule
  requête, le cache ne traverse donc pas les requêtes. Si le serveur passe en keep-alive, il faudra vider ce cache à chaque requête.
- **Anti-homonymes** (`pseudo_libre.py`) : contrôle avant insertion (message clair : « déjà pris » pour la forme canonique, « ressemble trop » pour le
  squelette) puis capture de `UniqueViolation` pour la course entre deux inscriptions, ce qui donne toujours un 409.
- **Frein** (`frein.py`) : 5 échecs en 15 minutes, par IP et par pseudo canonique, en mémoire (perdu au redémarrage, propre à un seul processus). L'IP
  vient de `X-Real-IP`, posé par le vhost nginx de l'hôte (`proxy_set_header X-Real-IP $remote_addr`), sinon de `client_address`. Un succès efface le
  compteur du pseudo, pas celui de l'IP. Le mot de passe demandé pour changer de mot de passe ou supprimer le compte est freiné de la même manière.
- **Compte hérité** (`mdp_hash` NULL) : la première connexion avec un mot de passe valide le fixe (`UPDATE ... WHERE mdp_hash IS NULL`, sûr en cas de
  course) et la réponse porte `"active": true`.
- **Suppression** : vérifie le mot de passe, retire d'abord les lignes `playlist_medias` qui référencent ses médias (clé `RESTRICT`, y compris dans les
  playlists des autres), supprime la ligne du compte (cascade), puis les fichiers (`<fichier>` et `<id>-mini.jpg`) et l'avatar.
- **Avatars** : fichiers sur disque (`DOSSIER_AVATARS/<id>.<ext>`), extension et version en base ; l'URL porte `?v=<version>`.
- **Routes GET** : elles renvoient elles-mêmes `401` au lieu de lever `Refus`, car `do_GET` n'attrape pas les `Refus`.

## Comptes invités éphémères

- `POST /api/anonyme` crée un compte `ephemere` (mdp_hash NULL, pseudo « Invité-NNNN », nouvel essai en cas de collision de pseudo). Frein : 20 créations par
  IP et par heure. Un compte éphémère ne peut jamais se connecter par pseudo/mot de passe (il n'est pas « activable » comme un compte hérité) et
  `POST /api/moi/mdp` répond 403.
- `purge.py` (`purger_compte`) sert à la suppression volontaire, à la déconnexion d'un invité et au nettoyage : transfert des médias présents dans la
  playlist d'un autre propriétaire (sauf si ce propriétaire a déjà la même référence YouTube), suppression du compte (cascade), suppression des médias
  orphelins d'autrui qui n'étaient que dans ses playlists, puis des fichiers et de l'avatar. Elle renvoie les comptes concernés ; l'appelant appelle
  `purge.signaler(comptes)` après validation (import paresseux de `diffusion.bibliotheque`). Les fichiers sont effacés dans la fonction, avant la
  validation de la transaction : un échec tardif peut laisser une ligne sans fichier.
- `nettoyage.py` : `purger_ephemeres_expires(cx)` (comptes éphémères sans session valide) et `nettoyer()` (transaction + signalement), à appeler
  périodiquement par l'orchestrateur.

## E-mail, récupération et offre

- L'adresse est facultative. `POST /api/moi/email` la place dans `email_en_attente` et envoie un lien (`jetons_courriel`, sha256 en base, 24 h, usage
  unique) ; `email` et `email_valide_le` ne sont écrits qu'à la confirmation (`confirmation.py`). L'unicité d'une adresse validée est garantie par un index
  unique sur `lower(email)` : la course entre deux confirmations se règle en 409. Un compte invité n'a jamais d'adresse. Frein : 5 envois par heure et par compte.
- Récupération (`recuperation.py`) : la demande répond toujours `{ok: 1}` (même sans compte ni adresse validée) ; le frein (5 par heure) porte sur l'IP
  et sur l'identifiant saisi, qu'il existe ou non, pour ne rien révéler. Le jeton (1 h) n'est valable que si l'adresse du compte est toujours celle du jeton.
  Le changement de mot de passe révoque toutes les sessions et en ouvre une neuve.
- Offre : `offre` (`free`/`pro`), attribuée par `administrer.py`. `envoi_fichiers` = Pro ET adresse validée ; le contrôle est dans `medias/autorisation.py`.
