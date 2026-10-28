# bdd

Accès à PostgreSQL. `adresse.py` compose l'URL (variable `BDD_URL`, sinon hôte/port/nom/utilisateur et mot de passe lu dans `BDD_MDP_FICHIER`,
jamais dans l'environnement ni dans le dépôt). `connexion.py` tient un pool (2 à 16 connexions) ; `transaction()` valide à la sortie du bloc et
annule sur exception. `migrations.py` applique dans l'ordre les fichiers `migrations/NNN_nom.sql` non encore listés dans la table `migrations`.

## Décisions

- Les migrations s'écrivent en SQL, ne se modifient jamais une fois poussées : un changement = un nouveau fichier.
- Un verrou consultatif (`pg_advisory_xact_lock`) sérialise les migrations, au cas où deux processus démarreraient ensemble.
- Chaque migration s'exécute dans la transaction de `migrer` : échec = rien d'appliqué.
- Identifiants en texte (16 caractères hexadécimaux) et non en UUID : les identifiants de playlist servent d'adresse de room et ceux de
  l'existant sont conservés tels quels à la migration.
- Le pseudo a deux index uniques, `pseudo_canonique` (casse, Unicode normalisé) et `pseudo_squelette` (ce qui se voit : accents, séparateurs
  et homoglyphes retirés). C'est le dernier verrou contre les homonymes ; la logique de calcul vit dans `comptes/`.
- Un média appartient à un compte ; `playlist_medias` interdit sa suppression tant qu'une playlist le contient (`RESTRICT`).
- L'état de lecture des canaux reste en mémoire (il change chaque seconde et se reconstruit au redémarrage).
