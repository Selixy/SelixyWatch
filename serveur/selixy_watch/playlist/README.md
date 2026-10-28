# playlist

Pistes d'une playlist (`playlist_medias`). Routes : `POST /api/playlist/<id>/<ajouter|retirer|deplacer>` `{media, avant?}`.
`actions.py` (façade : droit « editeur », crochets, signalement) ; `pistes.py` (les trois opérations SQL) ; `ajout_youtube.py` (utilisé
par l'import de liens).

## Décisions

- Un média n'est qu'une fois dans une playlist (409). Ajouter exige que le média soit visible du compte : le sien, ou présent dans une
  playlist qu'il peut lire (`bibliotheque.visibilite`). Sinon 404 « média inconnu ».
- Retirer : `canaux.synchro.avant_retrait` d'abord (passer au suivant si le média est en cours), puis suppression, puis nettoyage des
  orphelins. `canaux.synchro.playlist_modifiee` clôt chaque modification.
- Ordre par `rang` ; « avant » décale les rangs supérieurs ou égaux (sans le média déplacé).
- `ajouter_youtube` : média dédoublonné par (propriétaire, référence YouTube), il appartient au compte qui importe. Il revérifie le droit
  d'édition à chaque ajout (les droits ont pu changer pendant l'import) et ne signale rien : `liens.suivi` publie par lots.
