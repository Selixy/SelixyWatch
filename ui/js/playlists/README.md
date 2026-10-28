# Page Playlists

`ui/js/playlists.js` est la façade : elle branche les modules ci-dessous, démarre l'état partagé et réexporte `rendre`.
À gauche l'arbre des dossiers et playlists, à droite les pistes de la playlist choisie. Chaque playlist est aussi une room : « Entrer » y emmène.

## Modules

- `page.js` : état mutable de la page (`P` : sélection, playlist affichée, nœud ou piste en cours de glisser, renommage, rendu en attente), message d'erreur, `essayer`. `rendre` est un observateur : `rendu.js` s'y enregistre via `definirRendu`, ce qui évite les imports circulaires.
- `stockage.js` : `localStorage` protégé (stockage indisponible = valeur par défaut, écriture ignorée), dossiers ouverts, playlist affichée.
- `elements.js` : éléments du DOM utilisés par plusieurs modules.
- `rendu.js`, `arbre-rendu.js`, `vue-pistes.js` : rendu de l'arbre et de la playlist choisie.
- `arbre-evenements.js`, `actions-arbre.js`, `actions-pistes.js` : clics, clavier, création, renommage, suppression, ajout et retrait de pistes.
- `glisser-arbre.js`, `glisser-arbre-decision.js`, `glisser-pistes.js`, `indicateurs.js`, `depot.js` : glisser-déposer.
- `envoi.js`, `miniature.js`, `pochette-mp3.js`, `jpeg.js` : envoi de fichiers et miniatures.
- `liens.js`, `recherche.js` : liens YouTube et Spotify, recherche YouTube.

## Pièges et décisions

- Un clic sur une ligne ne refait pas l'arbre : un rendu entre les deux clics casserait le double-clic. La classe `select` et `vue-courante` est déplacée à la main.
- Pendant un glisser ou un renommage (`P.glisse`, `P.piste`, `P.edition`), `rendrePage` ne dessine rien et note `P.enAttente` ; le rendu repart à la fin du glisser (`dragend`) ou du renommage.
- Après création d'un nœud, `rendre()` est rappelé : le flux a pu livrer le nouveau nœud avant la réponse de l'API, et `P.aRenommer` déclenche alors le renommage.
- Position de dépôt dans l'arbre : sur un dossier, le quart haut = avant, le milieu = dedans, le quart bas = après ; sur une playlist, moitié haute = avant, moitié basse = après.
- La recherche porte un jeton : une recherche plus récente rend la réponse précédente caduque. Un lien YouTube ou Spotify collé s'importe directement (vidéo, playlist, album) ; un autre texte lance une recherche YouTube après 400 ms.
- Les erreurs d'import ne sont affichées qu'une fois (`surLiens`), et préfixées du nom de la playlist si ce n'est pas celle affichée.
- Une miniature est prise dans le navigateur : image de la vidéo (attente maximale de 8 s) ou pochette ID3 (balise APIC, 1 Mo lu au plus) ; ignorée au-delà de 200 Ko. En cas d'échec, l'icône sert de repli. La durée est lue par un élément `video` et envoyée dans `X-Duree`.
- Le champ ID3 de taille est « synchsafe » en v2.4 et un entier ordinaire en v2.3.

## Partage et droits

- `arbre-boutons.js` : boutons d'une ligne selon le rôle ; `actions-suppression.js` : suppression ou « Quitter » d'une racine reçue.
- Les actions de modification (renommer, supprimer, glisser, ajouter, importer, envoyer) sont masquées ou refusées pour un lecteur ;
  le rangement étant individuel, déplacer (glisser) et renommer sont permis sur tout élément visible, reçu ou non, vers n'importe quel dossier. Les racines de partage (`partage_racine: true`, champ de chaque nœud de `/api/bibliotheque`) portent l'avatar du propriétaire et gardent « Quitter ». Plus de dossier virtuel « Partagés avec moi ».
- Anonyme : la classe `anonyme` de la page n'affiche que l'appel à se connecter (`/#profil`).
- `ouverture.js` (+ `ouverture-chemin.js`, pur) : ouvre un dossier ou une playlist précis (le dossier lui-même et ses ancêtres dépliés). Le bouton « Inviter » de la barre ouvre `partager/inviter.js`. Sources : message `ouvrir` de la coque, ou clé
  `localStorage['mu-dossier']` (lue à chaque rendu, puis effacée). Si le nœud n'est pas encore dans la bibliothèque, la demande attend
  10 s (la relecture arrive par SSE).

## Envoi de fichiers réservé aux comptes Pro

`droit-envoi.js` lit `envoi_fichiers` du profil (`initCompte`) : sinon le bouton « Importer » est remplacé par une mention (`messages-envoi.js`,
pur et testé) et `envoyer` refuse aussi les dépôts de fichiers. Les liens YouTube/Spotify ne sont pas concernés. Le serveur reste l'autorité :
les échecs 402, 403 et 507 d'un envoi s'affichent avec leur message. Le droit est lu au chargement de la page ; après une validation d'e-mail il
faut recharger.
