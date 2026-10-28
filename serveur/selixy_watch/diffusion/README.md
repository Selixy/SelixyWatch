# diffusion

Envoi d'événements SSE aux abonnés (`ABONNES`).

- `bibliotheque.py` : `signaler(comptes)` envoie l'événement `bibliotheque {}` aux abonnés dont `ident` est dans l'ensemble. L'interface
  relit alors `GET /api/bibliotheque`. L'événement `arbre` a disparu. Les comptes concernés sont calculés par l'appelant, avant une suppression.
