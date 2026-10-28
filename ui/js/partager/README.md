# partager

Deux fenêtres modales en verre (fermées par Échap ou clic dehors, `fenetre.js`).

- **Inviter** (`inviter.js`, bouton « Inviter » de la barre de la vue Playlists, ou bouton du panneau d'un élément) : arbre de MES éléments
  (rôle `proprietaire`, hors « Partagés avec moi ») avec cases à cocher. Cocher un dossier coche et grise son contenu (il est couvert) ;
  seuls les ids de plus haut niveau partent dans `POST /api/invitations {noeuds, usages_max, jours}`. Un élément sélectionné à l'ouverture
  est pré-coché. Le lien complet (`location.origin + lien`) n'est montré qu'à la création (le serveur n'en garde que l'empreinte), avec la
  liste de ce qu'il partage.
- **Partager un élément** (`panneau.js`) : invités (retrait) et invitations actives (ce que couvre chaque lien, révocation du lien entier).
  Un seul rôle d'invité, éditeur : aucun choix de rôle. Lecture : `GET /api/partage?noeud=<id>` ; actions :
  `POST /api/partage/<id>/<retirer|revoquer|quitter>`.

Fichiers : `selection.js` (couverture et ids de plus haut niveau, logique pure), `propres.js` (mes éléments, bascule d'une case),
`rendu.js` et `rendu-inviter.js` (HTML), `requetes.js`, `lien.js`.
