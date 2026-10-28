# outils/audit

Mesure du dépôt complet, appelée par `../audit-modulaire.sh`. Python 3 sans
dépendance. Vue d'ensemble, écarts et règle de la liste d'exceptions dans
`../README.md`.

- `audit.py` : point d'entrée, argument `--racine`, bilan et code de sortie ;
- `inventaire.py` : chemins candidats, `git ls-files -co --exclude-standard` si la
  racine est celle d'un dépôt git, sinon parcours de l'arbre. Piège rencontré : le
  crochet de livraison locale (retiré depuis) testait un export `git archive`, sans `.git` ; `git ls-files` y
  sortait en code 128 et faisait échouer la livraison du 2026-10-03 ;
- `perimetre.py` : fichiers mesurés (exclusions) et type de mesure ;
- `lexeur_c.py`, `lexeur_diese.py` : lecteurs de caractères qui renvoient le texte
  *masqué* (chaînes, commentaires, expressions régulières, documents ici
  remplacés par des blancs, retours à la ligne conservés) et le nombre de
  commentaires ;
- `masquage.py`, `vue.py` : aiguillage par type, découpe d'un composant Vue ;
- `fonctions.py`, `longueurs.py` : détection des fonctions et de leur longueur sur
  le texte masqué ;
- `ecarts.py` : écarts d'un fichier ; `exceptions.py` : liste d'exceptions.

Arbitrage : tout est mesuré sur le texte masqué, pour qu'une chaîne ou un
commentaire qui contient `function`, `{` ou `#` ne fausse ni le comptage ni
l'appariement des accolades.
