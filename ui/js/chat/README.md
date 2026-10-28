# chat

Une conversation par playlist. `ui/js/chat.js` est la façade (`initChat`). `ui/js/notifs.js` fait partie du même domaine (messages du chat
par-dessus la vidéo) et reste un seul fichier.

- `affichage.js` : rendu de la liste `#messages` (100 messages au plus, défilement collé en bas sauf si on a remonté de plus de 80 px).
- `init.js` : réception des événements `chat`, envoi du formulaire.

## Pièges

- Les 100 derniers messages arrivent à l'ouverture du flux (événement `chat` avec `messages`), puis chaque message en direct (`message`).
- L'écoute est branchée tout de suite : l'historique peut arriver avant de savoir qui on est ; il est réaffiché une fois le compte connu
  pour repérer ses propres messages.
- Écrire demande un compte ; les anonymes lisent seulement. Mes messages font toujours défiler la liste.
- Si l'envoi échoue, le texte revient dans le champ et l'erreur s'affiche dans `#message`.

## notifs.js

Les messages du chat montent sur la vidéo quand le chat est replié : en plein écran avec le chat fermé, ou sur téléphone quand la file de
lecture est devant. Désactivables par la cloche de l'en-tête du chat ; le réglage (`mu-notifs`) reste dans ce navigateur. Trois
notifications au plus, chacune part après 4,8 s. Le stockage local peut être indisponible : les lectures et écritures sont protégées.
