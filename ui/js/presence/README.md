# presence

Liste des icônes sous le lecteur (comptes connectés dans la même room) et réactions emoji qui flottent sur la vidéo.
`ui/js/presence.js` est la façade (`initPresence`).

- `liste.js` : rendu de `#presents` à partir de `S.presence.canaux[room]`. Les nouveaux arrivent en animation, les partants s'effacent
  300 ms avant de disparaître. La première passe se fait sans animation.
- `reactions.js` : menu d'emojis et animation des réactions reçues.
- `init.js` : démarrage (réactions, vocal, clic sur un participant pour ouvrir son menu profil).

## Pièges

- `S.presence.canaux[room]` ne contient que les comptes connectés : les anonymes ne sont pas comptés.
- Les réactions passent par le serveur (événement `reaction`) : tout le monde dans la room les voit, mais seuls les comptes connectés
  peuvent réagir ; le bouton reste caché tant qu'on ne sait pas qui on est.
- L'écoute des réactions est branchée avant l'ouverture du vocal : le flux peut déjà être ouvert.
