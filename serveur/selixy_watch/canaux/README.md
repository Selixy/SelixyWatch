# canaux

État de lecture des rooms (une room = une playlist). L'état reste en mémoire (`CANAUX`, persisté dans `canaux.json`) ; l'ordre des pistes et
la durée des médias se lisent en base via `bibliotheque.lecture`, avec une connexion `cx` passée en premier paramètre à tout ce qui en a besoin.

- `acces_salle.compte_autorise(cx, h, cid)` : exige le rôle lecteur (401 anonyme, 404 room inconnue ou sans droit : on ne révèle pas l'existence).
  Utilisé par les commandes, le chat, les réactions et le signal vocal.
- `publication.publier(cx, cid, e)` : diffuse l'événement `canal` aux abonnés du canal et aux comptes `concernes` de la playlist, jamais aux autres.
- `synchro.py` : points d'entrée appelés par la bibliothèque quand une playlist change. `avant_retrait` (à appeler AVANT la suppression en base :
  il lit l'ordre courant pour passer au suivant), `playlist_modifiee` (normalise, arrête si le courant a disparu, diffuse), `playlist_supprimee`
  (oublie l'état du canal et les états vocaux).
- `rattrapage.horloge` ouvre une transaction par seconde ; une erreur de base est ignorée pour ne pas tuer le fil.

## Décisions

- Le comportement de lecture (avance, boucle, aléatoire, occupation, rattrapage) est inchangé ; seules les sources de données ont changé.
- Les routes de commande restent exportées par `route.py` (`ROUTES_POST`).
- Limite connue : un abonné SSE dont l'accès est retiré en cours de session garde son flux jusqu'à sa reconnexion.
