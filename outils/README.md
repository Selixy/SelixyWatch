# outils

## audit-modulaire.sh

Vérifie les règles de code du projet (voir le README principal) sur tout le dépôt. Option `--racine DIR`. Sortie : une ligne `ECART` par fichier fautif, `EXCEPTION PERIMEE` par exception
qui ne sert plus, puis le bilan ; code de sortie 1 au moindre écart.

Mesurés : `.js .mjs .cjs` `.py` `.sh` `.css` (hors `ui/visuels/`, les images). Écarts : `lignes` (> 200), `fonctions` (> 5 par fichier),
`longueur` (fonction > 50 lignes), `commentaires` (au moins un).

`audit-exceptions.txt` : l'existant hérité, une ligne par fichier (`chemin écart1,écart2`). Elle s'écrit à la main et ne peut que
décroître : un fichier retouché se met en conformité et sa ligne disparaît.
