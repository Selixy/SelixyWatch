# visuels

Tous les éléments visuels du projet sont ici (ils étaient dans `icones/`). La fiche `index.html` les montre tous : `/visuels/` sur le site. Le dossier est dans `ui/` : tout ce qu'il contient est servi
par le site sous `/visuels/`. Ne rien y mettre de privé.

## Utilisés par le site

- `favicon.svg`, `favicon-coupe.svg` : icône de l'onglet, sans et avec la lame rouge du mute. La page les remplace par une image dessinée à
  la volée (`js/marque/favicon.js`), ces fichiers servent de repli et de première image avant le script.
- `icone-180.png`, `icone-192.png`, `icone-512.png` : icônes d'application (écran d'accueil, manifeste). Fond sombre `#15141c`, logo clair
  à 80 % pour rester dans la zone de sécurité des icônes « maskable ».
- `partage.png` : image de partage (1200 × 630, `og:image` de `index.html`).
- `preparation.svg` : animation du voile de préparation du lecteur (logo seul en boucle, encre claire).

## Sources et essais

- `logotype-sombre.svg`, `logotype-clair.svg` : le logotype « SelixyWatch » (logo, puis « elixyWatch » en tracés, Roboto retouché), fond
  transparent. Le texte est le même que dans `js/marque/formes-texte.js`.
- `animation-logotype.svg` : l'animation complète du logotype (7 s en boucle : cadre, S qui s'écrit, pied, lame, lettres, fondu).
- `essais/curseur.svg` : essai de motion design. Le point du « i » devient un curseur de souris qui descend cliquer sur la télé : la lame
  rouge apparaît (mute), un second clic la retire, le curseur retourne sur le « i ». Les ondes marquent les clics.

## Pièges

- Ces fichiers ne sont pas écrits à la main : le dessin vient du S (courbes éditées dans un éditeur, recomposées en arcs de cercle) et de
  `js/marque/` (`construireMarque`) pour le logo ; le texte est la police Roboto (licence OFL) arrondie par calcul puis recomposée en
  tracés. Les scripts de fabrication sont hors dépôt (ils ne respectent pas les règles de taille) : en cas de refonte, repartir de
  `js/marque/formes.js` et `formes-texte.js`.
- Les SVG animés n'animent rien dans un `<link rel="icon">` : les images de l'onglet sont posées une à une par le script.
- Les animations sont en SMIL (natif, sans script) ; `prefers-reduced-motion` n'agit pas dessus : le site ne les pose pas dans ce cas.
