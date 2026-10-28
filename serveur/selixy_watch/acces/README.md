# acces

Droits sur un nœud (dossier ou playlist). `role_sur(connexion, compte, noeud)` renvoie `proprietaire`, `editeur`, `lecteur` ou `None` ;
`exiger(..., minimum)` lève 401 (pas de compte), 404 (aucun droit : on ne révèle pas qu'un élément existe) ou 403 (droit insuffisant).
`concernes(connexion, noeud)` donne les comptes à prévenir d'un changement (propriétaire et invités sur le nœud ou un de ses ancêtres).

## Décisions

- Un partage porte sur un nœud et vaut pour tout son sous-arbre : le rôle effectif est le plus fort trouvé sur la chaîne des ancêtres
  (requête récursive). Tous les nœuds d'un arbre ont le propriétaire de sa racine, même créés par un éditeur invité.
- Seul le propriétaire invite, retire un invité ou supprime la racine partagée.
