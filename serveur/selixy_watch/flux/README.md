# flux

Flux SSE `/api/flux`. Sans rôle lecteur sur `?canal=`, le flux est servi comme sans canal. Événements de départ : `canaux` (états des seules
playlists accessibles au compte ; vide pour un anonyme), puis `chat` (100 derniers) et `signal` si un canal est suivi. L'événement `arbre` n'existe
plus : l'interface relit `/api/bibliotheque` (événement `bibliotheque`). `ABONNES[q]` garde `{"canal", "ident"}`.

Aucune connexion à la base n'est tenue pendant la durée du flux : une transaction courte au départ et une à la fermeture.
