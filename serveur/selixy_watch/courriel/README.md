# Courriel

Envoi des deux messages du site (confirmation d'adresse, récupération de compte). Texte brut, en français, un seul lien.

- `envoi.py` : `envoyer(destinataire, sujet, texte)` renvoie `True` ou `False`, ne lève jamais d'exception (un échec est journalisé sur stderr,
  sans secret). `MAIL_URL` : `memoire` (tests, `BOITE_MEMOIRE`), `stdout` (local, défaut) ou l'URL d'un petit relais HTTP d'envoi de courriel
  (POST du message RFC 822 brut, `Authorization: Bearer`, `X-To`, `X-From`). Le secret est lu dans `MAIL_SECRET_FICHIER`
  (défaut `/secrets/mail_secret.txt`) à chaque envoi : jamais dans l'environnement ni le dépôt.
- `gabarits.py` : sujets et textes. Les liens portent le jeton dans le fragment (`#`) pour qu'il n'apparaisse pas dans les journaux nginx ;
  l'hôte vient de `URL_PUBLIQUE` (défaut `https://watch.selixy.dev`).

Pourquoi l'échec ne remonte pas : le relais peut refuser une adresse sans que l'utilisatrice y puisse quelque chose. La confirmation répond alors
`envoye: false` ; la récupération répond toujours pareil pour ne rien révéler.
