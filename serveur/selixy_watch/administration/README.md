# Administration

Commande `serveur/administrer.py` (base : `BDD_URL`). L'offre Pro est attribuée à la main, sans paiement.

- `pro PSEUDO [--quota-go N]` : refusée si le compte n'a pas d'adresse e-mail validée ; quota par défaut 20 Go.
- `free PSEUDO` : repasse en Free, quota 0. Les fichiers déjà envoyés restent (lecture, partage) : seul l'envoi est bloqué.
- `quota PSEUDO N` : fixe le quota en Go sans changer l'offre.
- `admin PSEUDO` / `retirer-admin PSEUDO` : compte administrateur = Pro illimité (aucun quota ; l'e-mail validé reste requis pour envoyer).
  Le propriétaire importé depuis le JSON devient admin.
- `lister` : pseudo, offre, e-mail validé, utilisé / quota.

Le contrôle d'envoi (offre Pro ou admin, ET e-mail validé, ET quota sauf admin) est dans `medias/autorisation.py` : un Pro qui change d'e-mail perd l'envoi tant que la
nouvelle adresse n'est pas confirmée, sans repasser en Free.
