# son

Le rond de l'en-tête coupe ou rétablit le son. C'est un réglage LOCAL : il vit dans ce navigateur (`localStorage`, clé `mu-muet`), n'est
jamais envoyé au serveur et ne change rien pour les autres. Le lecteur et le rond se préviennent par l'événement `son-local` de la
fenêtre ; le changement fait dans un autre cadre de la coque arrive par l'événement `storage`.

- `reglage.js` : lecture et écriture du réglage.
- `sourdine.js` : la sourdine forcée, quand le navigateur impose la sourdine (rien touché depuis le chargement). Le rond l'indique,
  comme le bouton du lecteur.
- `rond.js` : affichage et clic. Si la sourdine est forcée, le clic ne coupe pas : il rétablit le son (événement `rond-geste`, la room
  est prévenue).

## Volume général et mute général

Un seul réglage local pour tout le son de la page : `mu-volume` (0 à 1, 0,8 par défaut) et `mu-muet`. Le rond de l'en-tête, la jauge
de l'en-tête et le volume du lecteur écrivent les mêmes clés ; les autres cadres de la coque les suivent par l'événement `storage`.

- `volume-maitre.js` : lecture et écriture du volume général. Écrire un volume rétablit le son (`mu-muet` repasse à 0), comme le
  volume du lecteur.
- `jauge.js` : la jauge de l'en-tête. Elle remplace le texte « SelixyWatch » au survol, ou au focus venu du clavier (pas celui d'un clic : elle disparaît quand la souris sort,
  le focus de la souris est retiré) ; elle vaut 0 quand le son est
  coupé. Invisible sous 900 px, comme le texte : le rond reste le seul réglage sur téléphone.
- Le volume général multiplie le volume de la vidéo et celui des participants (par-dessus leur réglage individuel, voir `vocal/`).
- Le mute général coupe aussi le micro : voir `vocal/general.js`.
