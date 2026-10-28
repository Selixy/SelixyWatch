# ui

Petits outils d'affichage partagés. `../ui.js` est la façade.

- `dom.js` : `$` (querySelector) et `esc` (échappement HTML, à utiliser pour tout texte venu d'un utilisateur).
- `duree.js` : `3:07` ou `1:02:03`.
- `trace-icones.js`, `icone.js` : tracés SVG des icônes ; `play` et `pause` sont pleines, les autres sont des contours.
- `miniature.js` : l'image d'un média, dans l'ordre : vignette YouTube, image prise dans le fichier à l'envoi, et seulement en dernier
  recours l'icône (un fichier sans image : une musique sans pochette).
- `avatar.js` : l'image si elle existe, sinon l'initiale sur une teinte (`--h`) tirée du pseudo.

# Modules sans sous-dossier (`api.js`, `compte.js`, `main.js`, `debug.js`)

- `api.js` : renvoie toujours `{ ok, status, data }`, jamais d'exception pour une erreur HTTP (réseau coupé : `status` à 0).
- `compte.js` : le lien du compte dans l'en-tête est « Login » si anonyme, sinon avatar éventuel et pseudo, sans initiale de
  remplacement. Partagé par toutes les pages.
- `main.js` : page Room. Sans room (aucune mémorisée, ou supprimée) on retourne choisir une playlist, dans la coque comme seule.
  Les icônes sont posées par l'attribut `data-icone`, avant le texte du bouton.
- `debug.js` : diagnostic activé par l'adresse `/?debug`, pour relever sur un téléphone les derniers gestes et l'état des commandes
  du lecteur. N'existe que si l'adresse le demande.
