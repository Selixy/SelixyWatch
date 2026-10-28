# arbre

Dossiers et playlists d'un compte, en base (`noeuds`). Routes : `POST /api/arbre/<creer|renommer|deplacer|supprimer>` (`routes.py`,
`actions.py` en est la façade). Un fichier par action : `creation`, `renommage`, `deplacement`, `suppression` ; `lecture.py` (requêtes
récursives : profondeur, hauteur d'un sous-arbre, sous-arbre), `rangs.py` (ordre des frères), `orphelins.py` (médias sans playlist).

## Décisions

- Chaque action reçoit la connexion et l'identifiant du compte, et renvoie `(corps, comptes concernés)` ; `actions.py` ouvre la
  transaction (sous le verrou global, parce que les crochets de `canaux.synchro` touchent l'état en mémoire), puis signale les comptes
  après validation.
- Les droits viennent de `acces.droits.exiger` (404 si inconnu, 403 si insuffisant). Créer à `"racine"` = chez soi (`parent_id` NULL) ;
  créer sous un parent donne le propriétaire de l'arbre du parent, même pour un éditeur invité.
- Les comptes concernés d'une suppression sont calculés avant le `DELETE` ; ceux d'un déplacement avant et après (la visibilité change).
- Supprimer la racine d'un partage reçu (nœud partagé avec le compte, dont il n'est pas propriétaire) : 403, il faut « quitter ».
- Rangement individuel (migration 007, table `rangements`) : `deplacer` et `renommer` n'agissent que sur la vue du compte (`vue_perso.py`
  : cycle et profondeur 8 contrôlés dans cette vue ; `rangement.py` : écriture). Un nœud à soi déplacé vers la racine ou un dossier à soi met à
  jour `noeuds` (sa ligne `rangements` est supprimée) ; tout autre cas écrit une ligne `rangements`. Les droits ne lisent jamais les rangements.
  Seul le compte lui-même est signalé. Supprimer un dossier : les lignes `rangements` qui le visaient passent à parent NULL (racine).
- Limites : profondeur 8 (un dossier racine = niveau 1), 3000 nœuds par propriétaire d'arbre (507). Un déplacement contrôle aussi la hauteur du
  sous-arbre déplacé.
- Ordre : colonne `rang` ; insérer « avant » décale les rangs `>=` de ses frères. Les trous sont sans conséquence.
- Orphelins : après chaque suppression, tout média sans ligne dans `playlist_medias` est supprimé, fichier et miniature compris. Les fichiers
  sont effacés dans la transaction (un échec de validation à cet instant précis est très improbable et ne laisserait qu'un fichier de moins).
- `playlist_supprimee(pid)` (crochet des canaux) est appelé pour chaque playlist du sous-arbre supprimé.
