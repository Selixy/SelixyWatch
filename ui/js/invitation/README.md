# invitation

Page `/invitation/#<jeton>` : le jeton est dans le fragment pour ne jamais apparaître dans les journaux nginx. La page est autonome
(pas la coque) et ne charge que `invitation.css`, `login.css` et le socle.

Parcours :

1. `voir` (`POST /api/invitation/voir`, renvoie `noeuds`) affiche « <pseudo> vous invite à A », « à A et B » ou « à A, B et N autres »
   (un seul rôle d'invité : aucune mention de rôle). 404 et 410 sont traduits en phrases claires.
2. Pas connecté : le jeton est gardé dans `sessionStorage` (`invitation_en_attente`, partagé avec l'iframe de login de la coque, même
   onglet et même origine) et un bouton mène à `/#profil`. La page de login (`login/suite-connexion.js`) accepte ensuite le jeton.
3. Connecté : `accepterEtEntrer` accepte (`POST /api/invitation/accepter`), efface le jeton et entre dans le site.

- `jeton.js` : lecture du fragment, jeton en attente (stockage passé en paramètre, tolère un stockage indisponible).
- `acceptation.js` : appels `voir` / `accepter` (l'`api` se passe en paramètre) et textes d'erreur.
- `destination.js` : un seul élément : playlist → room, dossier → vue Playlists ; plusieurs : vue Playlists ouverte sur le premier. `entrerDans` écrit la clé de destination dans `localStorage` puis, depuis
  un cadre, prévient la coque (`entrer` pour une room, `recharger` pour Playlists) ; hors cadre, il change d'adresse.
- `suite.js` : branche tout cela sur le navigateur ; `phrase.js` : le texte d'invitation.

## Décisions

- Un dossier n'a pas de moyen d'être ouvert depuis l'extérieur : la clé `mu-dossier` (`localStorage`) porte l'identifiant à ouvrir ;
  la vue Playlists la lit au démarrage (`playlists/ouverture.js`), déplie le dossier lui-même ET tous ses ancêtres
  (dans la structure de la vue du compte), puis la retire. Défaut corrigé : seuls les ancêtres étaient dépliés, le dossier reçu arrivait replié.
- Le jeton n'est effacé qu'après une acceptation réussie, pour qu'une erreur réseau permette de réessayer.

## Mode anonyme éphémère

`anonyme.js` (créer le compte via `POST /api/anonyme`, avertissement, confirmation de déconnexion) vit dans `invitation/` car la page d'invitation et la connexion le partagent. Le serveur supprime le compte éphémère à la déconnexion : l'interface le dit (bandeau du profil, `confirm` avant de se déconnecter) et masque mot de passe et appareils (`data-permanent`).
