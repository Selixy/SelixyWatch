# vocal/echo

Annulation d'écho du micro avec le son du lecteur comme référence (le principe de Discord). L'annulation d'écho du navigateur ne voit pas
toujours ce que joue le lecteur ; ici on le soustrait nous-mêmes.

## Modules

- `index.js` : façade `filtrerMicro(piste, lecteurs)`. Passe la piste du micro dans un `AudioWorkletNode` à deux entrées (micro, référence)
  et rend la piste nettoyée. Au moindre échec (pas d'`AudioWorklet`…), la piste brute est rendue telle quelle. `stop()` de la piste rendue
  arrête aussi le micro brut et défait le graphe.
- `capture.js`, `reference.js` : la référence est la somme des éléments `<video>` et `<audio>` du lecteur (`captureStream`), pondérée par leur
  volume et leur sourdine (la capture ignore l'un et l'autre, l'écho non).
- `processeur.js` : le processeur audio, qui n'appelle que `annuleur.js`.
- `annuleur.js` : une ligne à retard (`retard.js`) puis un filtre adaptatif NLMS de 512 coefficients (`filtre.js`) qui estime l'écho et le retire,
  puis une atténuation résiduelle quand le reste du signal ne ressemble qu'à de l'écho.
- `porte.js` : porte de bruit après l'annulation, pour le son sans référence (YouTube). Elle s'ouvre quand le niveau dépasse 2,5 fois le fond
  sonore (et un plancher de 0,006), reste ouverte 0,3 s, referme à -20 dB. Le fond est le minimum récent du niveau : il tombe aussitôt
  qu'il y a un creux et ne remonte que lentement (6 s ouverte, 1 s fermée). Un apprentissage « moyen » avait pris la voix pour du fond
  et coupé le micro ; un son parfaitement continu (un bip) est, lui, bien traité comme du fond.
- `estimateur.js` : retard entre référence et micro, par corrélation des enveloppes (500 points par seconde, fenêtre d'une seconde, retard
  jusqu'à 0,5 s), refait toutes les 0,25 s. Le filtre ne couvre que 11 ms : le retard est donc estimé à part et décalé de la moitié du filtre.

## Pièges et arbitrages

- Seuls les lecteurs de fichiers ont une référence. L'iframe YouTube est une autre origine : son son est inaccessible à la page, donc rien
  n'est retiré de ce côté (il reste l'annulation d'écho du navigateur).
- Les voix des autres participants ne sont pas dans la référence (un seul retard estimé) : l'annulation d'écho du navigateur reste activée
  sur le micro brut pour elles.
- Le pas d'adaptation est faible (0,05) et sans détecteur de double parole : la voix agit comme un bruit qui ralentit un peu la convergence
  mais ne la dérègle pas. Convergence : environ une demi-seconde après la détection du retard, soit 1 à 1,5 s après le début du son.
- L'atténuation résiduelle (gain 0,15) joue seulement quand la puissance de l'erreur est sous 30 % de celle de l'écho estimé : une voix
  même plus faible que l'écho passe.
- Non mesuré dans un vrai navigateur : le retard réel entre `captureStream` et le micro, et la tenue de la capture quand la source change,
  sont à vérifier. Les tests (`tests/ui/echo.test.js`) simulent un écho avec retard et réponse de salle, pas une vraie salle.
