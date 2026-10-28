# etat

État partagé et synchronisation de toutes les pages. Le serveur garde l'arbre des dossiers et playlists, les médias, l'état de lecture
de chaque playlist (un canal d'écoute, ou « room ») et la présence, et les diffuse en SSE. `../etat.js` est la façade : tous les
modules importent de là, jamais d'ici.

- `partage.js` : l'objet `S` (noeuds, medias, canaux, imports, presence, canal écouté, decalage d'horloge, pret) et `maintenant()`
  (heure serveur = heure locale + décalage, en secondes).
- `observateur.js` : `surChangement` (abonnement à tout changement d'état, `notifier(quoi)` avec `arbre`, `canal`, `autre-canal`,
  `import`, `presence`) et `surEvenement` (événements propres à une room : `chat`, `reaction`, `signal`, via `diffuser`).
- `arbre.js`, `libelles.js` : lecture de l'arbre (noeud, enfants, chemin « Séries › Saison 1 », nom, ordre des pistes).
- `canal.js` : état de lecture d'un canal et position cible (`cible` extrapole `pos` depuis `t0` si la lecture est en cours).
- `requetes.js` : `poster` renvoie `r.data` ou lève une `Error` portant le message du serveur ; `action`, `actionPlaylist` et
  `actionArbre` n'en sont que des habillages.
- `horloge.js`, `flux.js`, `messages.js`, `selection.js`, `demarrage.js` : étalonnage, connexion SSE, traitement des messages, choix
  de room, démarrage.
- `stockage.js` : `localStorage` protégé (navigation privée, stockage bloqué : on retombe sur la valeur par défaut).

## Pièges et décisions

- Étalonnage de l'horloge : 6 échantillons espacés de 120 ms, on garde celui dont l'aller-retour est le plus court ; l'écart est
  `t_serveur + rtt/2 - t_reçu`. Chaque navigateur se cale sur l'horloge du serveur, ce qui fait entendre à tout le monde la même seconde.
- `messages.js` reçoit `reconnecter` en paramètre : quand la playlist écoutée n'existe plus (message `arbre`), il faut quitter la
  room, effacer `mu-canal` et rouvrir le flux sans canal. Le paramètre évite une dépendance circulaire avec `flux.js`.
- `entrer` : dans la coque, la room est déjà chargée dans un autre cadre, donc on la prévient par `postMessage` au lieu de recharger ;
  cela évite aussi que le cadre des playlists ne s'abonne au canal de la room, afin que seule la room réelle compte dans l'occupation.
  Hors coque on navigue vers `/#room`.
- `demarrer(avecCanal)` et `connecter(avecCanal)` : les playlists démarrent avec `avecCanal = false` pour ne pas être comptées dans
  l'occupation d'une room.
- `choisirCanal` rouvre le flux : le serveur n'envoie l'historique du chat qu'à la connexion, avec le canal en paramètre.
- Les événements `chat`, `reaction`, `signal` ne passent pas par `S` : ils sont éphémères et dépendent de la room.

## Bibliothèque par compte

- `bibliotheque.js` : lit `GET /api/bibliotheque` (noeuds, medias) à l'ouverture du flux SSE (`open`, aussi après une reconnexion
  automatique) et à chaque événement `bibliotheque`, regroupé par `regroupement.js` (pas plus d'une lecture toutes les 120 ms ; une
  demande pendant une lecture en provoque une seconde). Le changement est toujours notifié sous le nom `arbre` (= « bibliothèque relue »).
- `construction.js` : `lireReponse` (401 = anonyme, erreur réseau = on garde l'état) ; les nœuds sont ceux du serveur, tels quels
  (plus de dossier virtuel).
- `droits.js`, `droits-arbre.js` : droits d'affichage selon `role` (`proprietaire`, `editeur`, `lecteur`) : modifier, déplacer, partager,
  racine reçue (`partage_racine`, on la quitte au lieu de la supprimer), déplacement et renommage permis sur tout élément visible
  (vers « racine » ou un dossier visible), parent de création.
- `S.anonyme` (pas de session) et `S.refuse` (la room écoutée a disparu de la bibliothèque : plus d'accès) alimentent les messages de la
  room et de la page Playlists.
- Le serveur filtre déjà ; ces droits ne servent qu'à masquer ce qui serait refusé.
