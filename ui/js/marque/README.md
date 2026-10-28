# marque

Le logo de SelixyWatch (une télé que traverse un S) et sa lame. La lame est l'indicateur « son coupé » : elle apparaît quand le son
est coupé, elle se retire quand il est rétabli. Elle s'affiche à deux endroits, avec le même rythme : le bouton de l'en-tête et le
favicon de l'onglet. Le bouton garde l'identifiant `#rond-son` (c'est le même bouton, `son/rond.js` le pilote), il n'est plus rond.

- `formes.js` : les chemins du logo, en données. Le S, la fente du cadre, le cadre, le pied, la lame et son jour sont des arcs de
  cercle calculés hors du dépôt à partir de la forme dessinée (4 points de contrôle pour la spine du S, tracé vectorisé ensuite).
- `lame-rythme.js` : le rythme, deux séquences (`apparition`, `disparition`) avec courbes de Bézier d'accélération. Une seule source
  pour l'en-tête et le favicon. L'épaisseur ne bouge pas : à la taille de l'en-tête (30 px) et du favicon, un amincissement ou un dépassement ne se voit pas. Le
  rythme complet (fil, impact avec dépassement de 20 %, amincissement avant retrait) existe seulement dans `visuels/preparation.svg`,
  l'animation du voile de préparation, qui est grande.
- `lame-geometrie.js` : passage d'un état (`largeur` de 0 à 1, `epaisseur`) à la fenêtre de révélation et à l'échelle de la lame.
- `defs-formes.js`, `defs.js` : les définitions SVG (clips, masques). Les masques font passer chaque pièce devant ou derrière : la lame
  passe devant le milieu du S et devant la barre basse, derrière le haut du S et derrière la barre haute.
- `logo.js` : le SVG complet du logo (`construireMarque`). Sans lame quand `largeur` vaut 0. `echelleS` réduit le S (l'en-tête le met à
  0,9 : moins grand, il dépasse moins au-dessus de la télé).
- `chronologie.js` : boucle d'animation (`requestAnimationFrame`) d'une séquence.
- `entete.js` : monte le logo dans le bouton et joue la lame.
- `favicon-image.js`, `favicon.js` : le favicon. À chaque image le logo est dessiné dans un canvas, puis posé dans `<link rel="icon">`.
- `formes-texte.js`, `mot.js` : le mot « elixyWatch » (le S est celui du logo), en tracés (sans police), une lettre par chemin. Dans l'en-tête,
  c'est un élément à part du logo : il est collé au logo mais centré en hauteur sur ses propres lettres. Le texte est de Roboto
  (licence OFL) retouché : « elixy » en italique atténué de 4° avec coins arrondis (rayon 0,9) et point du « i » rond, « Watch » droit
  avec coins arrondis (rayon 0,45). La boîte du mot est taillée autour de ses lettres et centrée sur la hauteur des capitales (pour que le mot paraisse centré
  verticalement dans la barre), descendante du « y » comprise. Le logo, lui, est centré par sa propre boîte : le bas de la télé et la
  ligne de base du texte ne coïncident donc plus, c'est voulu. Le mot prend la couleur du texte de la page (`currentColor`).
- `voile.js` : le voile « préparation » (`/visuels/preparation.svg`, logo seul en boucle, encre claire car il se pose sur l'image de la
  room, toujours sombre). Il s'accroche à la zone qu'on lui donne ; c'est le lecteur qui décide quand (`js/lecteur/preparation.js`).
- `index.js` : façade, `initMarque(bouton, lien).definirCoupe(coupe)`. Le favicon ne se pilote que dans la page principale.
  Rien ne s'anime au premier appel (le chargement de la page). Rappeler
  avec le même état ne fait rien.

## Pièges

- Un favicon SVG animé ne s'anime pas dans un onglet : le mouvement du favicon est une suite d'images (une toutes les 80 ms pendant
  la transition) posées une à une. Si le dessin dans un canvas échoue, repli sur `favicon.svg` / `favicon-coupe.svg` (deux états,
  sans transition).
- `prefers-reduced-motion` : l'en-tête saute directement à l'état final, sans animation.
- L'encre du favicon suit `prefers-color-scheme` (le fond de l'onglet est celui du navigateur, pas celui de la page).
- Les attributs `data-rev` et `data-echelle` repèrent la fenêtre et l'échelle de la lame à animer : ils portent une valeur vide, car
  le SVG doit rester du XML valide (il sert aussi seul, comme image du favicon).
- Si l'état change pendant une animation, la nouvelle part de son début (un saut visible, rare).
