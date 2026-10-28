# login

Page login et profil. Anonyme : deux modes, Connexion et Inscription (pseudo + mot de passe de 8 à 128 caractères, confirmation à
l'inscription). Connecté : renommer le compte, avatar facultatif (réduit dans le navigateur avant l'envoi), changement de mot de
passe, appareils connectés, déconnexion partout, suppression du compte, espace utilisé.

- `saisie.js` : état du formulaire de profil (profil enregistré, avatar choisi mais pas encore envoyé, retrait demandé).
- `regles.js` : contrôles de saisie purs (testés) et choix du texte d'erreur : le message du serveur est affiché tel quel (409
  homonyme, 401), avec un repli pour 429.
- `mode.js`, `authentification.js` : bascule Connexion/Inscription, envoi vers `/api/connexion` ou `/api/inscription`.
- `suite-connexion.js` : après une connexion réussie. Compte hérité (`active: true`) : « Mot de passe enregistré » puis suite. Si un
  jeton d'invitation attend (voir `../invitation/README.md`), il est accepté et on entre sur l'élément partagé ; sinon retour à la room.
- `profil.js` : active les sections réservées aux connectés. `mdp.js`, `sessions.js` (+ `sessions-rendu.js`), `suppression.js`, `quota.js`.
- `affichage.js`, `reduction.js`, `choix-avatar.js`, `envoi.js`, `redirection.js` : aperçu, avatar, enregistrement du pseudo, retour.

## Pièges

- Dans la coque, c'est elle qu'on recharge pour revenir à la room (`postMessage` `recharger`) ; seule, la page va à `/#room`. Après un
  enregistrement, la coque est prévenue (`compte`) pour mettre à jour son en-tête.
- Un compte déjà connecté qui change de mot de passe déconnecte les autres appareils (côté serveur) ; la session courante reste.
- La suppression du compte redemande le mot de passe : un cookie volé ne suffit pas.
- L'appareil d'une session est deviné à la volée depuis l'agent utilisateur (`sessions-rendu.js`) : approximatif, affichage seulement.

## Anonyme

Le bouton « Entrer en anonyme » suit le même chemin qu'une connexion (`suite-connexion.js`), invitation en attente comprise. Le profil d'un compte éphémère n'a ni mot de passe ni appareils, mais un bandeau d'avertissement.

## Adresse e-mail, offre, mot de passe oublié

- `email-etat.js` (pur, testé) : état de la carte (aucune / en attente / validée), contrôle de saisie, textes d'erreur. `email.js` : la carte
  « Adresse e-mail » (`POST /api/moi/email`, `/api/moi/email/supprimer`) ; « Renvoyer le lien » rejoue l'enregistrement de l'adresse en attente.
  Chaque action redemande le mot de passe, puis relit `GET /api/moi`. Carte masquée pour un compte éphémère (`data-permanent`).
- Administrateur (`admin`) : carte « Administrateur · stockage illimité » ; `quota: null` = illimité, la jauge dit « <utilisé> utilisés · illimité ».
- `offre-etat.js` (pur, testé), `offre.js` : carte « Offre ». Free : texte seulement ; Pro : jauge `quota.js`, plus une note tant que
  `envoi_fichiers` est faux.
- `oubli.js` : « Mot de passe oublié ? » (`POST /api/recuperation`). La réponse est toujours le même message neutre, que le compte existe ou non.
- Les pages `/confirmer/` et `/recuperation/` (`ui/js/confirmer*`, `ui/js/recuperation*`) lisent leur jeton dans le fragment (`invitation/jeton.js`),
  l'effacent de l'adresse (`history.replaceState`) et ne l'envoient que dans le corps d'un POST. Après récupération, le serveur pose la session.
