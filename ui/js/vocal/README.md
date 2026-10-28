# vocal

Chat vocal et vidéo WebRTC maillé (pair à pair) dans la room. `ui/js/vocal.js` est la façade : ses exports ne changent pas.

## Modules

- `etat.js` : état partagé (`vocal`, `monEtat`) et lecture de l'état d'un participant (`etatDe`, `estMoi`).
- `signal.js` : envoi d'un message de signalisation (`POST /api/canal/<id>/signal`).
- `ecoute.js` : réception des messages `signal` du flux SSE (`/api/flux`), aiguillés vers `signal-etats.js` (états micro/caméra,
  départs) et `signal-webrtc.js` (offre, réponse, candidats ICE) par une table d'actions (stratégie).
- `pairs.js` : une `RTCPeerConnection` par pair, pistes reçues, élément `<audio>` caché par pair.
- `medias.js` : micro et caméra, deux supports décrits par une table (`SUPPORTS`) qui partage les mêmes étapes d'activation et de coupure.
- `echo/` : annulation d'écho du micro avec le son du lecteur comme référence (voir son `README.md`). `supports.js` : table micro/caméra de `medias.js`.
- `voix-analyse.js`, `voix.js` : indicateur de parole. Un `AnalyserNode` par participant (micro local ou piste reçue) lit le spectre ;
  `voix.js` en tire un niveau lissé (0 à 1) écrit dans `--voix` sur son avatar et pose la classe `parle` au-dessus d'un seuil. Le CSS
  (`css/presence-voix.css`) en fait un grossissement et un halo.
- `volume.js` : volume et mute locaux par pair (jamais envoyés aux autres). Le volume joué est le réglage du pair multiplié par le volume
  général (`son/volume-maitre.js`) ; le mute général coupe tous les pairs. `volume-calcul.js` : ce calcul seul, sans DOM (testé).
- `general.js` : réagit au mute et au volume généraux (`son-local`, `storage`). Au passage en mute, le micro est coupé s'il était actif ; au
  retour du son, il est rétabli seulement s'il avait été coupé par ce mute (comme le « sourd » de Discord). On peut rallumer le micro
  à la main pendant un mute : rien ne le recoupe avant le prochain changement de mute.
- `affichage.js` : badge et vidéo dans `#presents`. `taille.js` : tailles des caméras et des avatars.
- `menu.js`, `menu-html.js` : menu profil (volume individuel, mute, micro, caméra).
- `init.js` : branchement unique au démarrage.

## Pièges et arbitrages

- Pour éviter deux offres simultanées entre deux pairs, seul celui dont l'identifiant est le plus grand appelle.
- L'élément `<video>` d'un participant est toujours muet, sinon écho : le son passe par l'élément `<audio>` caché de `pairs.js`.
- Le serveur STUN est celui de Google ; pas de serveur TURN : deux pairs derrière des NAT symétriques ne se verront pas.
- Après une action du menu profil (micro, caméra, mute), `ouvrirMenuProfil` est rappelé alors que le menu est encore enregistré comme
  ouvert pour ce participant : il se ferme. Comportement d'origine conservé tel quel.
- Une erreur sur `getUserMedia` (refus, absence de périphérique) affiche une alerte et ne change pas l'état.
- Les caméras sont dimensionnées pour tenir toutes dans la zone : `meilleureTaille` essaie chaque nombre de colonnes et garde la plus grande taille
  qui tient en largeur et en hauteur (hauteur = jusqu'au bas de la fenêtre moins 28 px, largeur et marges de la zone retirées, 14 px réservés au
  mouvement des avatars). Chaque avatar sans caméra compte pour 0,3 caméra. Entre 48 et 240 px ; sous 48 px ça déborde plutôt que de devenir illisible.
  La zone passe à la ligne (`flex-wrap`) au lieu de défiler. Les avatars sans caméra font 28 à 48 px selon leur nombre ; avec une caméra, 28 % de la
  taille des caméras (26 à 46 px).
- L'indicateur de parole mesure la bande 375 à 3750 Hz (cases 2 à 19 d'une FFT de 256 à 48 kHz), donc la voix et peu le bruit grave. Le
  niveau monte vite (0,5 par image) et redescend lentement (0,12) pour éviter le scintillement. Il ne dépend ni du volume réglé ni de la
  sourdine locale : on voit qu'une personne parle même si on a coupé son son. `AudioContext` démarre suspendu sans geste : il est repris à
  chaque nouvelle analyse (activation du micro ou arrivée d'une piste). Avec `prefers-reduced-motion`, plus de grossissement, seulement le halo.
- Un `AnalyserNode` branché sur un flux distant ne reçoit des données que si ce flux est aussi lu par un élément `<audio>` : c'est le cas (`pairs.js`).
- Le micro est demandé avec `echoCancellation`, `noiseSuppression`, `suppressLocalAudioPlayback` et `voiceIsolation` (le gain automatique est coupé : il remonte le niveau de l'écho entre deux phrases) : l'annulation d'écho du navigateur retire du micro le son que la page joue (vidéo de la room, voix des pairs). Elle ne retire pas un son joué par une autre application ni un autre onglet ; avec des enceintes à fort volume, le casque reste la solution fiable.
