# ui/js/lecteur

Lecteur de la room : vidéo ou audio synchronisé sur l'état du serveur, commandes par-dessus l'image, file de lecture, raccourcis.
`../lecteur.js` est la façade : il n'exporte que `initLecteur` et `rendreSon` (la coque signale un geste, clic sur le rond de l'en-tête).
La position affichée et visée vient de l'état du serveur (`cible()`), jamais du lecteur : tout le monde voit et entend la même chose.

## Organisation

- `contexte.js` : éléments du DOM et état partagé `L` (lecteur en service, son bloqué, volume, dernier geste…), à la place de variables de module.
- `evenements.js` : observateur minimal (`sur`, `emettre`). Il coupe les cycles d'import : les lecteurs émettent (`yt-pret`, `yt-etat`,
  `yt-erreur`, `pub-finie`, `son-a-appliquer`), `synchro.js` et `volume.js` écoutent.
- `fichier.js` : lecteur d'un élément `<video>`/`<audio>`, paramétré par une *origine* (`url(id, m)`, `arreter()`) : fichier du serveur, ou flux
  YouTube (`flux/`). `youtube*.js` : lecteur iframe, de nouveau utilisé par `fabrique.js` (le flux ne tient pas : YouTube refuse l'IP du serveur, voir
  `flux/README.md`). Les événements souris sont coupés sur l'iframe (`pointer-events: none`) : le clic traverse jusqu'à notre interface et
  YouTube n'affiche plus ses commandes au survol. `fabrique.js` choisit selon `media.source`.
- `flux/` (non branché dans `fabrique.js`, en attente d'une IP de sortie acceptée par YouTube) : YouTube lu par notre propre lecteur (Media Source Extensions). `origine.js` donne l'URL d'un `MediaSource`, `session.js` le
  nourrit toutes les 500 ms (40 s d'avance), `piste.js` charge les segments d'une piste (vidéo ou audio) d'après l'index `sidx` lu par
  `mp4.js`, `tampon.js`/`attente.js`/`plages.js`/`segments.js` enveloppent le `SourceBuffer`, `reseau.js` interroge `/flux/`.
- `synchro.js` : `caler()` aligne le lecteur en service sur l'état du serveur ; boucles d'une seconde (dérive) et de 500 ms (pubs).
- `volume.js`, `reglages-son.js`, `deblocage.js`, `autorisation.js`, `poster.js` : son local, sourdine imposée, image d'attente YouTube.
- `preparation.js`, `preparation-etapes.js` : le voile de préparation sur l'image du lecteur (logo animé, `marque/voile.js`). Il
  couvre le cas où, à l'entrée dans la room ou après un rechargement, l'état du canal n'est pas arrivé ou le média n'est pas prêt
  (`preparee()` du lecteur s'il en a un, sinon `pret()`). Il n'apparaît qu'après 600 ms d'attente, on abandonne après 20 s, et il part dès que
  le lecteur est prêt : pas de durée minimale, sinon la vidéo tourne déjà dessous et on a l'impression qu'on y touche. Pour YouTube,
  `pret()` dit seulement que la commande de chargement est partie ; `preparee()` attend que YouTube soit réellement en lecture, en pause ou
  en attente (états 1, 2, 5), pas en chargement (-1, 3). Le voile ne se joue
  qu'une fois par chargement de la page : ensuite, une mise en mémoire en cours de lecture ne le rappelle pas. `preparation-etapes.js`
  est la décision seule, sans DOM (testée).
- `affichage.js`, `file.js`, `progression.js`, `indicateur.js`, `repos.js` : rendu et commandes qui s'effacent.
- `commandes.js`, `actions.js`, `clavier.js`, `pointeur.js` : entrées de la personne. `plein.js`, `chat-plein.js`, `cinema.js`,
  `salle-etat.js`, `disposition.js` : modes de la salle. `demarrage.js` : `initLecteur`, qui branche tout.

## Contrat des lecteurs (stratégie)

`charger(id, m, e)`, `pret()`, `occupe()` (pub en cours : on ne force rien), `position()`, `duree()`, `aller(s)`, `recaler(but)`, `jouer()`,
`pause()`, `estEnPause()`, `volume(v)`, `muet(b)`, `vider()`, `reinitialiser()` (remet à zéro les temporisations de saut, au retour sur la page),
plus `finesse` (écart de position toléré en pause). Le fichier ajoute `estElement(v)` pour ignorer les événements de l'élément inactif.
Une nouvelle source = un nouveau module qui respecte ce contrat, enregistré dans `fabrique.js`.

## Pièges et arbitrages

- Le navigateur refuse le son tant que la personne n'a rien touché : `lire()` lance alors la lecture en sourdine (`L.bloque`), l'image avance
  synchronisée et le son revient au premier geste n'importe où sur le site (`debloquer`). `getAutoplayPolicy` sert quand il existe, sinon
  `userActivation.hasBeenActive`. Le toucher qui rétablit le son (`L.premierGeste`, 700 ms) ne doit ni mettre en pause ni couper le son.
- Un élément `<audio>` lit la musique (il continue écran verrouillé, surtout sur iPhone), `<video>` le reste. Les réglages de son sont locaux :
  jamais envoyés au serveur ni aux autres.
- Dérive du fichier : un petit écart se rattrape en accélérant ou ralentissant à peine (jusqu'à 7 %) parce qu'un saut vide la mémoire
  tampon et fait ramer, surtout sur téléphone. Au-delà de 2,5 s on saute, au plus une fois toutes les 4 s (8 s si ça charge).
- YouTube n'a que des vitesses fixes : un saut explicite ou un écart de plus de 2,5 s saute immédiatement ; une dérive mineure (1,2 à 2,5 s) saute au plus une fois toutes les 3 s. `aller()` commande le lecteur actif immédiatement pour une réponse directe de la barre de progression. L'API IFrame est chargée une seule fois, à la première vidéo YouTube. États YT : -1 non démarré, 0 fini, 1 lecture, 2 pause, 3 mise en mémoire, 5 prêt.
- Pubs YouTube : l'API ne les signale pas. `youtube-pub.js` les devine toutes les 500 ms sans jamais agir sur le lecteur (drapeau `enPub`) : vidéo en cours différente de celle voulue, ou durée annoncée nettement éloignée de celle du média (3 s ou 2 %). Les sauts et mises en tampon légitimes ne sont pas pris pour des pubs.
- `jouer()` de YouTube est résolu quand ça joue et rejeté (« bloqué ») si rien ne démarre en 4 s, ce qui déclenche le repli en sourdine.
- Le lecteur YouTube affiche logo, titre et « Plus de vidéos » à l'arrêt : une image de la vidéo (`#poster`) le recouvre tant que la room
  est en pause ou que la lecture est bloquée.
- Préchargement : les deux prochaines pistes (fichiers) se chargent dans des `<video>` cachés ; les fichiers de 30 Mo ou moins sont aussi
  lus d'avance dans le cache, sauf en mode économie de données.
- Commandes : elles se masquent après 2,5 s sans geste, sauf doigt posé, pause, survol ou focus clavier. Au doigt, toucher l'image affiche
  ou masque les commandes sans toucher à la lecture ; jamais masquer ce qu'un toucher vient d'afficher (700 ms). À la souris, un clic =
  lecture/pause (attend 250 ms de savoir si un second clic suit), un double-clic = plein écran.
- Raccourcis clavier : la touche Espace fait lecture/pause inconditionnellement partout sur la page et depuis la coque parente (sauf si un champ de texte est ciblé, ex. `#chat-texte`). Cela évite que le navigateur n'active par défaut le dernier bouton ayant le focus (cinéma, plein écran, muet, etc.) ou ne fasse défiler la page.
- Plein écran : c'est toute la salle qui passe en plein écran (écran plus chat qui glisse par-dessus). Sans API de plein écran (iPhone), la
  salle recouvre la page et la coque masque son en-tête (message `plein` vers le parent).
- Téléphone : la file et le chat sont deux cartes empilées ; celle qu'on choisit passe devant, l'autre devient `inert`.
- Retour sur la page (écran déverrouillé) : on rejoint la room tout de suite sans attendre la boucle d'une seconde.
- Diagnostic : l'adresse `/?debug` charge `../debug.js`.
- Flux YouTube : le service `flux/` relaie deux pistes MP4 fragmentées (vidéo H.264, audio AAC) ; le navigateur les assemble dans un seul
  `<video>`. L'état à charger se déduit toujours de la fin du tampon contigu à la position : pas d'index mémorisé, donc un saut ou un
  retour en arrière ne demande aucun cas particulier. `ManagedMediaSource` (iPhone, iOS 17.1 et plus) est utilisé à défaut de
  `MediaSource` ; avant, ou si les codecs ne passent pas, `flux-erreur` fait passer à la suite. Non vérifié sur iPhone.
- Tests : `node --test tests/ui/*.test.js` (analyse `sidx`, chargement des segments avec un tampon factice, annulation d'écho).
- Échec du flux (`flux-erreur`) : message et pause de la room, jamais de saut à la suivante. Sauter relançait une résolution YouTube par
  vidéo en rafale et faisait bloquer l'IP du serveur.
