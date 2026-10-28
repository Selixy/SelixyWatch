# polices

« SelixyWatch Sans » : la police de tout le site (`--sans` dans `css/tokens.css`, déclarée par `css/police.css`). C'est Roboto (Christian
Robertson, Roboto Project Authors, licence SIL Open Font License 1.1, texte dans `OFL.txt`) dont les coins des lettres sont arrondis, et
dont les points presque carrés (i, j, point, deux-points, point d'exclamation, tréma) sont devenus ronds.

- Quatre fichiers WOFF2, une graisse chacun : 400, 500, 600, 700. Pas d'italique : le site n'en utilise pas.
- Sous-ensemble de 336 caractères : latin de base, Latin-1, Latin étendu A (œ, Œ…), ponctuation courante (– — ‘ ’ “ ” … « » •), €, flèches.
  Un caractère hors de cette liste retombe sur la police suivante de la pile (`system-ui`, `Segoe UI`, `Roboto`, `sans-serif`).
- Espacement (chasses), kerning et accents sont ceux de Roboto : seuls les contours des glyphes simples ont été redessinés.
- Fabriquée hors du dépôt avec fontTools et shapely : fermeture puis ouverture de la forme avec un rayon de 4,5 % de l'em, réduit glyphe
  par glyphe quand il détruirait un détail fin (le rayon effectif est surtout réduit sur la graisse 400, dont les traits sont les plus fins).
- Le logotype de l'en-tête n'utilise pas cette police : ses lettres sont des tracés (`js/marque/formes-texte.js`).

## Pièges

- La licence OFL impose de garder le texte de la licence et la mention de copyright avec la police : ils sont dans la table `name` des
  fichiers et dans `OFL.txt`. Une version modifiée ne peut pas se vendre seule.
- À 14-15 px l'arrondi se voit à peine : il se remarque surtout sur les titres et les grandes tailles.
- Pas de hinting : le rendu sur écran basse définition (Windows, anciens écrans) n'est pas vérifié.
- Les fichiers sont servis avec `Cache-Control: no-cache` comme le reste (règle `location /` du nginx) : le navigateur les revalide à chaque
  visite (réponse 304). Un cache long demanderait de changer la configuration nginx.
