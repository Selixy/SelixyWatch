# coque

La coque choisit la vue affichée (Room, Playlists, Profil) sans jamais décharger les autres. Une vue est un cadre (`iframe`) chargé à
sa première visite : la room reste en vie, et sa lecture continue, quand on va dans les playlists. Les vues lui parlent par
`postMessage` (même origine seulement) : `entrer`, `aller`, `recharger`, `compte`, `sourdine`, `plein`.

- `cadres.js` : accès aux cadres et au canal mémorisé.
- `vues.js` : affichage d'une vue, onglet courant, navigation par `#hash`. Sans room mémorisée, la vue Room redirige vers Playlists.
  La room reçoit le focus : ses raccourcis clavier en dépendent.
- `messages.js` : table des commandes reçues des cadres (une entrée par type de message).
- `zones.js` : zones sûres (encoche, barre d'état, indicateur d'accueil) mesurées ici et copiées dans les cadres en variables CSS
  `--sa-t`, `--sa-r`, `--sa-b`, `--sa-l`, car `env()` n'est pas fiable dans un cadre.
- `clavier.js` : quand le clavier s'ouvre, la zone visible rétrécit (iOS ne redimensionne pas la page). La coque suit
  `visualViewport` (`--hauteur`, `--decalage`, classe `decale`) pour que la saisie du chat reste au-dessus du clavier. Un pincement de
  zoom (`scale > 1.01`) est ignoré.

## Pièges

- Le plein écran « sans API » (iOS) masque l'en-tête de la coque (classe `plein`).
- Le rond de l'en-tête, quand le son est bloqué par le navigateur, envoie l'événement `rond-geste` : la coque le transmet à la room,
  car ce clic est le geste utilisateur dont elle a besoin pour rétablir le son.

## Ouverture directe par le hash

`ouverture.js` : `#playlists/<id>` ouvre la vue Playlists sur ce dossier ou cette playlist ; `#room/<id>` entre dans la room de cette
playlist. `<id>` = 12 caractères hexadécimaux. La coque transmet (message `ouvrir` ou `room` si le cadre est chargé, sinon clé
`mu-dossier` ou `mu-canal`), puis réécrit le hash en `#playlists` ou `#room`.
